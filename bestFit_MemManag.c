// last edit: 10.4. 15:50

/*
* Memory management library based on Worst-fit algorhitm
*
* Created by Dávid Beòo
*/

#include <stdint.h>
#include "bestFit_MemManag.h"


/*
First two block in linked list
*/
static Mem_block Start, *End = NULL;

/*
Actual free memory
*/
uint16_t actFreeMem = FREE_SRAM - sizeof(Start) - sizeof(Start); // 2 * MEM_BLOCK_SIZE



static void insertNewBlock(Mem_block *pNewBlockToInsert);

static void joinBlock(Mem_block *pAct);

static void deleteFromList(Mem_block* toDel);

void bPrintLinkedList();

/* ********* IMPORTAT ************** 
* IF pNextFreeBlock points to Start, it means, block is allocated
* else block is free.
* 
* pPrevBlock can point to start but block can be free
*/


void bMemInit() {

	Mem_block *pNewBlock;
	char *ptr = (char*)&Start;
	actFreeMem = FREE_SRAM - sizeof(Start) - sizeof(Start);


	/*Initialises start of linked list*/
	Start.pNextFreeBlock = NULL;
	Start.pPrevBlock = NULL;
	Start.blockSize = 0;

	/*shift pointer*/
	ptr += MEM_BLOCK_SIZE;
	pNewBlock = (Mem_block*)ptr;

	/* New block represents whole free memory, insert between pStart and pEnd */
	pNewBlock->pNextFreeBlock = End;
	pNewBlock->pPrevBlock = &Start;
	pNewBlock->blockSize = actFreeMem - MEM_BLOCK_SIZE;
	Start.pNextFreeBlock = pNewBlock;

	/*shift pointer*/
	ptr += (MEM_BLOCK_SIZE + pNewBlock->blockSize);
	End = (Mem_block*)ptr;
	

	/*Initialises end of linked list*/
	End->pNextFreeBlock = NULL;
	End->pPrevBlock = pNewBlock;
	End->blockSize = FREE_SRAM;

	pNewBlock->pNextFreeBlock = End;

	actFreeMem -= MEM_BLOCK_SIZE;

}


void *bMemAlloc(uint16_t requestedSize) {
	char *ptr;
	void *toReturn = NULL;	// pointer which will be returned
	Mem_block *pPrev;		// pointer to previous block
	Mem_block *pAct;		// pointer to actual block
	Mem_block *pNew;		// pointer to new block

	/* Cannot allocate 0 bytes*/
	if (requestedSize < 0) {
		return NULL;
	}

	/*For better computing -- this condition can be deleted*/
	if (requestedSize % 2 != 0) {
		requestedSize++;
	}

	/*If requested size is still lower than actual free space in memory*/
	if (requestedSize <= actFreeMem) {

		/*We allocate memory for request and for new block*/
		requestedSize += MEM_BLOCK_SIZE;

		pPrev = &Start;
		pAct = pPrev->pNextFreeBlock;

		/* Finding best block to allocate*/
		while ((pAct->pNextFreeBlock != NULL) && (pAct->blockSize <= requestedSize)) {

			/*Exactly right block was found. No need to create new block, created one will be used*/
			if (pAct->blockSize == (requestedSize - MEM_BLOCK_SIZE) || pAct->blockSize == requestedSize ) {
				break;
			}

			pPrev = pAct;
			pAct = pAct->pNextFreeBlock;
		}

		/*Found free block. Block size and requested size matches*/
		if (pAct->pNextFreeBlock != NULL && (pAct->blockSize == (requestedSize - MEM_BLOCK_SIZE) || pAct->blockSize == requestedSize)) {

			toReturn = (void*)((char*)pAct + MEM_BLOCK_SIZE);	// pointer to block which will be returned
			pPrev->pNextFreeBlock = pAct->pNextFreeBlock;		// actual block is deleted from list of free blocks
			actFreeMem -= (requestedSize - MEM_BLOCK_SIZE);						// actual free memory is decreased
			pAct->pNextFreeBlock = &Start;						// allcated block points to the Start of memory
			
		}

		/*Found free block. Requested size is bigger than blocksize of actual block.
		New block will be created and insert to linked list of free blocks.*/
		if (pAct->pNextFreeBlock != NULL && pAct->blockSize > requestedSize) {
			
			/*requestedSize = request + size of BLOCK, because pointer must jump over actual block and requested size of memory.
			It ends on the begginig of new block*/
			pNew = (Mem_block*)((char*)pAct + requestedSize); 

			/*Actual free memory space is decreased
			Space for new block is counted in requestedSize*/
			actFreeMem -= requestedSize;

			/*New block is filled with its data*/
			pNew->blockSize = pAct->blockSize - requestedSize;
			pNew->pNextFreeBlock = NULL;
			pNew->pPrevBlock = pAct;

			/*Update of actual block*/
			pAct->blockSize = requestedSize - (MEM_BLOCK_SIZE);

			/*actual block is deleted from list of free blocks*/
			pPrev->pNextFreeBlock = pAct->pNextFreeBlock;

			/*Insert new block to linked list of free blocks*/
			insertNewBlock(pNew);

			/*pointer to block which will be returned*/
			toReturn = (void*)((char*)pAct + MEM_BLOCK_SIZE);

			/*Set pPrevBlock to the next block - set to actual block*/
			ptr = (char*)pNew;
			ptr += MEM_BLOCK_SIZE + pNew->blockSize;
			pPrev = (Mem_block*)ptr;
			pPrev->pPrevBlock = pNew;

			/*allocated block points to the Start of memory*/
			pAct->pNextFreeBlock = (Mem_block*)&Start;
		}
	}

	return (void*)toReturn;
}



/*
ak je vytvoreny novy blok pouzije sa funckia insertNewBlock
ak sa ale zlucuje viacero blokov, to znamena ze jeden uz bol v liste zvacsil sa (priradil sa k inemu)
Nikdy sa nebudu vyskytovat 2 a viac volnych blokov vedla seba, preto ak uvolnujem blok, maximalne mozu byt okolo neho 1 volny blok pred aj za.
Preto netreba prehladavat bloky v cykle ale staci sa pozriet iba na jeden pred a jeden za
*/

void bMemFree(void *ptrToFree) {
	Mem_block *block;
	Mem_block *next;
	char *ptr = (char*)ptrToFree;
	int chR = 0, chL = 0;

	if (ptrToFree != NULL) {

		/*Jump on the beginning of block*/
		ptr -= MEM_BLOCK_SIZE;

		/*Cast to Mem_block type*/
		block = (Mem_block*)ptr;
		insertNewBlock(block);
		actFreeMem += block->blockSize;

		/*Try to join right next block*/
		ptr = (char*)block;
		ptr += MEM_BLOCK_SIZE + block->blockSize;
		next = (Mem_block*)ptr;
		if (next->pNextFreeBlock != &Start && next != End) {
			joinBlock(block);
			
		}

		next = block;
		block = block->pPrevBlock;
		/*Try to join left*/
		if (block != &Start && block->pNextFreeBlock != &Start) {
			joinBlock(block);
			
		}
		
	}

}


void *bMemRealloc(void *ptrToRealloc, uint16_t requestedSize) {
	void *toReturn = NULL;	// pointer which will be returned
	Mem_block *pBlock = NULL;
	Mem_block *pNext;
	Mem_block *pNewBlock;
	Mem_block *pNextToNew;
	char *ptr = (char*)ptrToRealloc;
	char* pNew = (char*)ptrToRealloc;
	int i;
	char needToCopy = 'N';

	if (requestedSize < 0) {
		return NULL;
	}
	
	if (ptrToRealloc != NULL) {

		/*First check if copying data is needed*/
		ptr -= MEM_BLOCK_SIZE;
		pBlock = (Mem_block*)ptr;
		i = pBlock->blockSize;

		ptr += MEM_BLOCK_SIZE + pBlock->blockSize;
		pBlock = (Mem_block*)ptr;

		if ((pBlock->pNextFreeBlock == &Start) || (i + pBlock->blockSize + MEM_BLOCK_SIZE < requestedSize)) {
			needToCopy = 'Y'; 
		}
		else {
			needToCopy = 'N';
		}

		
		/*If copying data is not needed*/
		if (needToCopy == 'N') {

			ptr = (char*)ptrToRealloc;
			ptr -= MEM_BLOCK_SIZE;
			pBlock = (Mem_block*)ptr;

			ptr += MEM_BLOCK_SIZE + pBlock->blockSize;
			pNext = (Mem_block*)ptr;

			ptr += MEM_BLOCK_SIZE + pNext->blockSize;
			pNextToNew = (Mem_block*)ptr;

			/*If new block will not be created. New size matches size of actual block and size of next free block*/
			if (i + pBlock->blockSize + MEM_BLOCK_SIZE == requestedSize) {

				i = pNext->blockSize;
				deleteFromList(pNext);

				pBlock->blockSize += i + MEM_BLOCK_SIZE;
				pNextToNew->pPrevBlock = pBlock;

				toReturn = (char*)pBlock + MEM_BLOCK_SIZE;

				actFreeMem -= i;

			}
			/*New block will be created*/
			else {

				ptr = (char*)ptrToRealloc;
				ptr += requestedSize;
				pNewBlock = (Mem_block*)ptr;

				i = pNext->blockSize;
				deleteFromList(pNext);

				bPrintLinkedList();

				pNewBlock->pPrevBlock = pBlock;
				pNewBlock->blockSize = i - (requestedSize - pBlock->blockSize);
				actFreeMem -= requestedSize - pBlock->blockSize;

				pNextToNew->pPrevBlock = pBlock;

				pBlock->blockSize = requestedSize;

				insertNewBlock(pNewBlock);

				toReturn = (char*)pBlock + MEM_BLOCK_SIZE;

			}

		}


		// toto kopirovanie by malo byt fixnute
		/*If it is needed to copy data*/
		if (needToCopy == 'Y') {

			/* Allocate new block of memory */
			toReturn = bMemAlloc(requestedSize);

			/* Copy data if allocation was successfull */
			if (toReturn != NULL) {
				ptr = (char*)ptrToRealloc;
				ptr -= MEM_BLOCK_SIZE;
				pBlock = (Mem_block*)ptr;

				/*Set pointers to copying*/
				pNew = (char*)toReturn;
				ptr += MEM_BLOCK_SIZE;

				if (requestedSize >= pBlock->blockSize) {
					for (i = 0; i < pBlock->blockSize; i++) {
						pNew[i] = ptr[i];
					}
				}

				if (requestedSize < pBlock->blockSize) {
					for (i = 0; i < requestedSize; i++) {
						pNew[i] = ptr[i];
					}
				}
				

				/* Make old pointer free*/
				bMemFree(ptrToRealloc);
			}
		}
		

	}
	

	return (void*)toReturn;
}

void bPrintLinkedList() {
	Mem_block *iterator = &Start;

	printf("\n\nList of free memory blocks\n");
	printf("Size of block %d\n", MEM_BLOCK_SIZE);

	/*Iterates whole list and prints size of each block from Start to penultimate block*/
	for (iterator = &Start; iterator->pNextFreeBlock != NULL; iterator = iterator->pNextFreeBlock) {
		printf("Block %d \n", iterator->blockSize);
	}
	/*Prints size of End block*/
	printf("Block %d \n", iterator->blockSize);

	/*Prints real actual free memory */
	printf("Celkovo volnej pamate je: %d \n", actFreeMem);
}

void bPrintWholeMemory() {
	Mem_block *iterator = &Start;
	char *ptr = (char*)iterator;

	printf("\nList of all blocks of memory \n");
	printf("Block %d START\n", iterator->blockSize);


	while (1) {
		ptr += (MEM_BLOCK_SIZE + iterator->blockSize);
		iterator = (Mem_block*)ptr;

		if (iterator->blockSize == FREE_SRAM) {
			break;
		}

		if (iterator->pNextFreeBlock == &Start) {
			printf("Block %d ALLOCATED\n", iterator->blockSize);
		}
		else {
			printf("Block %d FREE\n", iterator->blockSize);
		}

	}

	printf("Block %d END\n", iterator->blockSize);
	printf("Toto free memory size: %d\n", actFreeMem);

}

void bPrintWholeMemoryReverse() {
	Mem_block *iterator = End;

	printf("\nReverse list of all blocks\n");
	printf("Block %d END\n", iterator->blockSize);

	for (iterator = iterator->pPrevBlock; iterator->pPrevBlock != NULL; iterator = iterator->pPrevBlock) {
		if (iterator->pNextFreeBlock == &Start) {
			printf("Block %d ALLOCATED\n", iterator->blockSize);
		}
		else {
			printf("Block %d FREE\n", iterator->blockSize);
		}
	}

	printf("Block %d START\n", iterator->blockSize);
}


/* Private functions */


/*
* Insert new block of memory created after allocation to the linked list of all free memory blocks
* List is always sorted from the lowest to the largest block.
* New block is always inserted to the right place in the list, list stays sorted
* 
* @param pNewBlockToInsert New block of memory to insert
*/

static void insertNewBlock(Mem_block *pNewBlockToInsert) {
	Mem_block *iterator = &Start;
	Mem_block *pPrev;


	if (pNewBlockToInsert != NULL) {
		/*Find the right place in list for block to be inserted*/
		while (1) {
			if (iterator->blockSize >= pNewBlockToInsert->blockSize) {
				break;
			}
			pPrev = iterator;
			iterator = iterator->pNextFreeBlock;
		}

		/*Insert block*/
		pPrev->pNextFreeBlock = pNewBlockToInsert;
		pNewBlockToInsert->pNextFreeBlock = iterator;

	}
	
}


/* 
* Deletes block from linked list of free blocks. List stay oredered
*
* @param toDel Block which will be deleted from linked list
*/
static void deleteFromList(Mem_block* toDel) {
	Mem_block *iterator = &Start;
	Mem_block *pPrev;


	if (toDel != NULL) {
		/*Find place in list where toDel is stored*/
		while (1) {
			if (iterator == toDel) {
				break;
			}
			pPrev = iterator;
			iterator = iterator->pNextFreeBlock;
		}

		/*Delete block*/
		pPrev->pNextFreeBlock = toDel->pNextFreeBlock;

	}
}


/*
* Join two blocks
*/

static void joinBlock(Mem_block *block) {
	Mem_block *next;
	char *ptr;

	/*Get next physical block*/
	ptr = (char*)block;
	ptr += MEM_BLOCK_SIZE + block->blockSize;
	next = (Mem_block*)ptr;

	deleteFromList(block);
	deleteFromList(next);
	actFreeMem -= block->blockSize;
	actFreeMem -= next->blockSize;

	/*Make actual block bigger*/
	block->blockSize += MEM_BLOCK_SIZE + next->blockSize;

	/*Delete next block*/
	ptr = (char*)next;
	ptr += MEM_BLOCK_SIZE + next->blockSize;
	next = (Mem_block*)ptr;

	next->pPrevBlock = block;

	/*Insert new block*/
	insertNewBlock(block);
	actFreeMem += block->blockSize;

}

