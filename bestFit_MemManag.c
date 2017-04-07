// last edit: 7.4. 22:40

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
static Mem_block Start, *End;

/*
Actual free memory
*/
uint16_t actFreeMem = FREE_SRAM - sizeof(Start) - sizeof(Start); // 2 * MEM_BLOCK_SIZE



static void insertNewBlock(Mem_block *pNewBlockToInsert);

void bPrintLinkedList();



void bMemInit() {

	Mem_block *pNewBlock;
	char *ptr = (char*)&Start;
	actFreeMem = FREE_SRAM - sizeof(Start) - sizeof(Start);


	/*Initialises start of linked list*/
	Start.pNextFreeBlock = NULL;
	Start.blockSize = 0;

	/*shift pointer*/
	ptr += MEM_BLOCK_SIZE;
	pNewBlock = (Mem_block*)ptr;

	/* New block represents whole free memory, insert between pStart and pEnd */
	pNewBlock->pNextFreeBlock = End;
	pNewBlock->blockSize = actFreeMem - MEM_BLOCK_SIZE;
	Start.pNextFreeBlock = pNewBlock;

	/*shift pointer*/
	ptr += (MEM_BLOCK_SIZE + pNewBlock->blockSize);
	End = (Mem_block*)ptr;

	/*Initialises end of linked list*/
	End->pNextFreeBlock = NULL;
	End->blockSize = FREE_SRAM;

	actFreeMem -= MEM_BLOCK_SIZE;

}





void *bMemAlloc(uint16_t requestedSize) {

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

	/*We allocate memory for request and for new block*/
	requestedSize += MEM_BLOCK_SIZE;

	/*If requested size is still lower than actual free space in memory*/
	if (requestedSize < actFreeMem) {
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
			pNew->pNextFreeBlock = End;

			/*Update of actual block*/
			pAct->blockSize = requestedSize - (MEM_BLOCK_SIZE);

			/*actual block is deleted from list of free blocks*/
			pPrev->pNextFreeBlock = pAct->pNextFreeBlock;

			/*Insert new block to linked list of free blocks*/
			insertNewBlock(pNew);

			/*pointer to block which will be returned*/
			toReturn = (void*)((char*)pAct + MEM_BLOCK_SIZE);
		}
	}

	return (void*)toReturn;
}





void bMemFree(void *ptrToFree) {
	Mem_block *block;
	char *ptr = (char*)ptrToFree;

	if (ptrToFree != NULL) {

		/*Jump on the beginning of block*/
		ptr -= MEM_BLOCK_SIZE;

		/*Cast to Mem_block type*/
		block = (Mem_block*)ptr;

		/*Insert freed block to sorted linked list*/
		insertNewBlock(block);

		/*Amount of accessible memory is increased*/
		actFreeMem += block->blockSize;
	}
	

}


void *bMemRealloc(void *ptrToRealloc, uint16_t requestedSize) {
	void *toReturn = NULL;	// pointer which will be returned
	Mem_block *pBlock = NULL;
	char *ptr = (char*)ptrToRealloc;
	char* pNew;
	int i;

	if (requestedSize < 0) {
		return NULL;
	}
	
	if (ptrToRealloc != NULL) {

		ptr -= MEM_BLOCK_SIZE;
		pBlock = (Mem_block*)ptr;

		/* Allocate new block of memory */
		toReturn = bMemAlloc(requestedSize);

		/* Copy data if allocation was successfull */
		if (toReturn != NULL) {
			
			pNew = (char*)toReturn;
			ptr += MEM_BLOCK_SIZE;
			for (i = 0; i < pBlock->blockSize; i++) {
				pNew[i] = ptr[i];				
			}
		}

		/* Make old pointer free*/
		bMemFree(ptrToRealloc);
	}
	

	return toReturn;
}






void bPrintLinkedList() {
	Mem_block *iterator;

	printf("\n\nList of free memory blocks\n");

	/*Iterates whole list and prints size of each block from Start to penultimate block*/
	for (iterator = &Start; iterator->pNextFreeBlock != NULL; iterator = iterator->pNextFreeBlock) {
		printf("Velkost bloku %d \n", iterator->blockSize);
	}
	/*Prints size of End block*/
	printf("Velkost bloku %d \n", iterator->blockSize);

	/*Prints real actual free memory */
	printf("Celkovo volnej pamate je: %d \n", actFreeMem);
}




void bPrintWholeMemory() {
	Mem_block *iterator = &Start;
	int size = iterator->blockSize;
	
	char *ptr = (char*)iterator;

	printf("\nList of all blocks of memory\n");

	while (1) {
		if (iterator->blockSize == FREE_SRAM) {
			break;
		}
		size = iterator->blockSize;
		printf("Velkost bloku %d \n", size);
		
		ptr += (MEM_BLOCK_SIZE + size);

		iterator = (Mem_block*)ptr;

	}

	printf("Velkost bloku %d \n", iterator->blockSize);

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

