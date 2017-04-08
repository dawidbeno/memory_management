// last edit: 7.4. 23:36

/*
* Memory management library based on Worst-fit algorhitm
*
* Created by D�vid Be�o
*/

#include <stdint.h>
#include "worstFit_MemManag.h"


/*
First two block in linked list
*/
static wMem_block Start, *End;

/*
Actual free memory
*/
uint16_t actFreeMemW = FREE_SRAM - sizeof(Start) - sizeof(Start); // 2 * MEM_BLOCK_SIZE



static void insertNewBlock(wMem_block *pNewBlockToInsert);

void wPrintLinkedList();



void wMemInit() {

	wMem_block *pNewBlock;
	char *ptr = (char*)&Start;
	actFreeMemW = FREE_SRAM - sizeof(Start) - sizeof(Start);

	/*Initialises start of linked list*/
	Start.pNextFreeBlock = NULL;
	Start.blockSize = FREE_SRAM;

	/*shift pointer*/
	ptr += MEM_BLOCK_SIZE;
	pNewBlock = (wMem_block*)ptr;

	/* New block represents whole free memory, insert between pStart and pEnd */
	pNewBlock->pNextFreeBlock = End;
	pNewBlock->blockSize = actFreeMemW - MEM_BLOCK_SIZE;
	Start.pNextFreeBlock = pNewBlock;

	/*shift pointer*/
	ptr += (MEM_BLOCK_SIZE + pNewBlock->blockSize);
	End = (wMem_block*)ptr;


	/*Initialises end of linked list*/
	End->pNextFreeBlock = NULL;
	End->blockSize = 0;

	actFreeMemW -= MEM_BLOCK_SIZE;

}





void *wMemAlloc(uint16_t requestedSize) {

	void *toReturn = NULL;	// pointer which will be returned
	wMem_block *pPrev;		// pointer to previous block
	wMem_block *pAct;		// pointer to actual block
	wMem_block *pNew;		// pointer to new block

							/* Cannot allocate 0 bytes*/
	if (requestedSize < 0) {
		return NULL;
	}

	/*For better computing -- this condition can be deleted*/
	if (requestedSize % 2 != 0) {
		requestedSize++;
	}


	/*If requested size is still lower than actual free space in memory*/
	if (requestedSize < actFreeMemW) {

		/*We allocate memory for request and for new block*/
		requestedSize += MEM_BLOCK_SIZE;

		pPrev = &Start;
		pAct = pPrev->pNextFreeBlock;

		/*Found free block. Block size and requested size matches*/
		if (pAct->pNextFreeBlock != NULL && (pAct->blockSize == (requestedSize - MEM_BLOCK_SIZE) || pAct->blockSize == requestedSize)) {

			toReturn = (void*)((char*)pAct + MEM_BLOCK_SIZE);	// pointer to block which will be returned
			pPrev->pNextFreeBlock = pAct->pNextFreeBlock;		// actual block is deleted from list of free blocks
			actFreeMemW -= (requestedSize - MEM_BLOCK_SIZE);						// actual free memory is decreased

		}

		/*Found free block. Requested size is bigger than blocksize of actual block.
		New block will be created and insert to linked list of free blocks.*/
		if (pAct->pNextFreeBlock != NULL && pAct->blockSize > requestedSize) {

			/*requestedSize = request + size of BLOCK, because pointer must jump over actual block and requested size of memory.
			It ends on the begginig of new block*/
			pNew = (wMem_block*)((char*)pAct + requestedSize);

			/*Actual free memory space is decreased
			Space for new block is counted in requestedSize*/
			actFreeMemW -= requestedSize;

			/*New block is filled with its data*/
			pNew->blockSize = pAct->blockSize - requestedSize;
			pNew->pNextFreeBlock = &End;

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





void wMemFree(void *ptrToFree) {
	wMem_block *block;
	char *ptr = (char*)ptrToFree;

	if (ptrToFree != NULL) {

		/*Jump on the beginning of block*/
		ptr -= MEM_BLOCK_SIZE;

		/*Cast to Mem_block type*/
		block = (wMem_block*)ptr;

		/*Insert freed block to sorted linked list*/
		insertNewBlock(block);

		/*Amount of accessible memory is increased*/
		actFreeMemW += block->blockSize;
	}


}





void *wMemRealloc(void *ptrToRealloc, uint16_t requestedSize) {
	void *toReturn = NULL;	// pointer which will be returned
	wMem_block *pBlock = NULL;
	char *ptr = (char*)ptrToRealloc;
	char* pNew;
	int i;

	if (requestedSize < 0) {
		return NULL;
	}

	if (ptrToRealloc != NULL) {

		ptr -= MEM_BLOCK_SIZE;
		pBlock = (wMem_block*)ptr;

		/* Allocate new block of memory */
		toReturn = wMemAlloc(requestedSize);

		/* Copy data if allocation was successfull */
		if (toReturn != NULL) {

			pNew = (char*)toReturn;
			ptr += MEM_BLOCK_SIZE;
			for (i = 0; i < pBlock->blockSize; i++) {
				pNew[i] = ptr[i];
			}
		}

		/* Make old pointer free*/
		wMemFree(ptrToRealloc);
	}


	return toReturn;
}






void wPrintLinkedList() {
	wMem_block *iterator;

	printf("\n\n Vypis Listu \n");

	/*Iterates whole list and prints size of each block from Start to penultimate block*/
	for (iterator = &Start; iterator->pNextFreeBlock != NULL; iterator = iterator->pNextFreeBlock) {
		printf("Velkost bloku %d \n", iterator->blockSize);
	}
	/*Prints size of End block*/
	printf("Velkost bloku %d \n", iterator->blockSize);

	/*Prints real actual free memory */
	printf("Celkovo volnej pamate je: %d \n", actFreeMemW);
}


void wPrintWholeMemory() {
	wMem_block *iterator = &Start;
	int size = iterator->blockSize;
	char *ptr = (char*)iterator;

	printf("\nList of all blocks of memory\n");
	printf("Velkost bloku %d \n", size);


	ptr += MEM_BLOCK_SIZE;
	iterator = (wMem_block*)ptr;

	while (1) {
		if (iterator->blockSize == 0) {
			break;
		}
		size = iterator->blockSize;
		printf("Velkost bloku %d \n", size);

		ptr += (MEM_BLOCK_SIZE + size);

		iterator = (wMem_block*)ptr;

	}

	printf("Velkost bloku %d \n", iterator->blockSize);

}



/* Private functions */


/*
* Insert new block of memory created after allocation to the linked list of all free memory blocks
* List is always sorted from the largest to the lowest block.
* New block is always inserted to the right place in the list, list stays sorted
*
* @param pNewBlockToInsert New block of memory to insert
*/

static void insertNewBlock(wMem_block *pNewBlockToInsert) {
	wMem_block *iterator = &Start;
	wMem_block *pPrev;

	/*Find the right place in list for block to be inserted*/
	while (1) {
		if (iterator->blockSize <= pNewBlockToInsert->blockSize) {
			break;
		}
		pPrev = iterator;
		iterator = iterator->pNextFreeBlock;
	}

	/*Insert block*/
	pPrev->pNextFreeBlock = pNewBlockToInsert;
	pNewBlockToInsert->pNextFreeBlock = iterator;

}






