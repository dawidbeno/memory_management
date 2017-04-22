
#include "bestFit_MemManag_EEPROM.h"


uint16_t StartAddress = 0;
uint16_t EndAddress = EEPROM - MEM_BLOCK_SIZE_B;


/*
Actual free memory
*/
uint16_t actFreeMem = EEPROM - (2*MEM_BLOCK_SIZE_B); // 2 * MEM_BLOCK_SIZE


static void bPrintOneStruct(Mem_block block);
static void insertNewBlock(uint16_t newAddr, Mem_block pNewBlockToInsert);
static void joinBlock(uint16_t blockAddr, Mem_block block);
static void deleteFromList(uint16_t toDelAddr, Mem_block toDelBlock);
static void clearMem();


void bMemInit(){
  //clearMem();
  Mem_block block;
  uint16_t ptr = StartAddress;

  actFreeMem = EEPROM - (2*MEM_BLOCK_SIZE_B);

  /*Initialises start of linked list*/
  block.pNextFreeBlock = StartAddress + MEM_BLOCK_SIZE_B;
	block.pPrevBlock = NONE;
	block.blockSize = 0;
  eeprom_write_block(&block, (uint16_t*)ptr, MEM_BLOCK_SIZE_B);

  /*shift pointer*/
	ptr += MEM_BLOCK_SIZE_B;

  /* New block represents whole free memory, insert between pStart and pEnd */
  block.pNextFreeBlock = EndAddress;  //points to END
  block.pPrevBlock = StartAddress;
  block.blockSize = actFreeMem - MEM_BLOCK_SIZE_B;
  eeprom_write_block(&block, (uint16_t*)ptr, MEM_BLOCK_SIZE_B);

  /*shift pointer*/
  ptr += (MEM_BLOCK_SIZE_B + block.blockSize);

  block.pNextFreeBlock = NONE;
  block.pPrevBlock = (StartAddress + MEM_BLOCK_SIZE_B);
  block.blockSize = EEPROM;
  eeprom_write_block(&block, (uint16_t*)ptr, MEM_BLOCK_SIZE_B);

  actFreeMem -= MEM_BLOCK_SIZE_B;

}



uint16_t bMemAlloc(uint16_t requestedSize){
    uint16_t ptr = StartAddress;
    uint16_t toReturn = NONE;
    Mem_block pPrev, pAct, pNew;
    uint16_t actAddr;
    uint16_t prevAddr;
    uint16_t newAddr;

    /* Cannot allocate 0 bytes*/
	if (requestedSize < 0) {
		return NONE;
	}

  /*For better computing -- this condition can be deleted*/
	if (requestedSize % 2 != 0) {
		requestedSize++;
	}

  /*If requested size is still lower than actual free space in memory*/
  	if (requestedSize <= actFreeMem) {

      /*We allocate memory for request and for new block*/
      requestedSize += MEM_BLOCK_SIZE_B;

      prevAddr = ptr;
      eeprom_read_block(&pPrev, (uint16_t*)ptr, MEM_BLOCK_SIZE_B);

      actAddr = pPrev.pNextFreeBlock;
      eeprom_read_block(&pAct, (uint16_t*)pPrev.pNextFreeBlock, MEM_BLOCK_SIZE_B);

        /* Finding best block to allocate*/
  		while ((pAct.pNextFreeBlock != NONE) && (pAct.blockSize <= requestedSize)) {

  			/*Free block is found*/
  			if (pAct.blockSize == (requestedSize - MEM_BLOCK_SIZE_B) || pAct.blockSize == requestedSize ) {
  				break;
  			}

        prevAddr = actAddr;
  			pPrev = pAct;

        actAddr = pAct.pNextFreeBlock;
        eeprom_read_block(&pAct, (uint16_t*)pAct.pNextFreeBlock, MEM_BLOCK_SIZE_B);

  		}

      /*Found free block. Block size and requested size matches*/
  		if (pAct.pNextFreeBlock != NONE && (pAct.blockSize == (requestedSize - MEM_BLOCK_SIZE_B) || pAct.blockSize == requestedSize)) {

        toReturn = actAddr + MEM_BLOCK_SIZE_B;  // pointer to block which will be returned

        pPrev.pNextFreeBlock = pAct.pNextFreeBlock; // actual block is deleted from list of free blocks
        eeprom_write_block(&pPrev, (uint16_t*)prevAddr, MEM_BLOCK_SIZE_B);

        actFreeMem -= (requestedSize - MEM_BLOCK_SIZE_B);	 // actual free memory is decreased

        pAct.pNextFreeBlock = StartAddress;
        eeprom_write_block(&pAct, (uint16_t*)actAddr, MEM_BLOCK_SIZE_B);

  		}

      /*Found free block. Requested size is bigger than blocksize of actual block.
		New block will be created and insert to linked list of free blocks.*/
		if (pAct.pNextFreeBlock != NONE && pAct.blockSize > requestedSize) {

      /*requestedSize = request + size of BLOCK, because pointer must jump over actual block and requested size of memory.
			It ends on the begginig of new block*/
			newAddr = actAddr + requestedSize;

      /*Actual free memory space is decreased
			Space for new block is counted in requestedSize*/
			actFreeMem -= requestedSize;

      /*New block is filled with its data*/
			pNew.blockSize = pAct.blockSize - requestedSize;
			pNew.pNextFreeBlock = NONE;
			pNew.pPrevBlock = actAddr;

      /*Update of actual block*/
			pAct.blockSize = requestedSize - (MEM_BLOCK_SIZE_B);

      /*actual block is deleted from list of free blocks*/
			pPrev.pNextFreeBlock = pAct.pNextFreeBlock;
      eeprom_write_block(&pPrev, (uint16_t*)prevAddr, MEM_BLOCK_SIZE_B);

      /*Insert new block to linked list of free blocks*/
			insertNewBlock(newAddr, pNew);

      /*pointer to block which will be returned*/
			toReturn = actAddr + MEM_BLOCK_SIZE_B;

      /*Set pPrevBlock to the next block - set to actual block*/
			ptr = newAddr;
			ptr += MEM_BLOCK_SIZE_B + pNew.blockSize;
      eeprom_read_block(&pPrev, (uint16_t*)ptr, MEM_BLOCK_SIZE_B);
			pPrev.pPrevBlock = newAddr;
      eeprom_write_block(&pPrev, (uint16_t*)ptr, MEM_BLOCK_SIZE_B);

      /*allocated block points to the Start of memory*/
      pAct.pNextFreeBlock = StartAddress;
      eeprom_write_block(&pAct, (uint16_t*)actAddr, MEM_BLOCK_SIZE_B);

    }


    }

  return (uint16_t)toReturn;

}





uint16_t bMemRealloc(uint16_t ptrToRealloc, uint16_t requestedSize){
    uint16_t toReturn;
    Mem_block pBlock, pNextBlock, pNewBlock, pNextToNewBlock;
    uint16_t pBlockAddr, pNextAddr, pNewAddr, pNextToNewAddr;
    uint16_t ptr = ptrToRealloc;
    uint16_t i;
    char needToCopy = 'N';

    if (requestedSize < 0) {
		    return NONE;
	  }

    if(ptrToRealloc < EEPROM){
        /*First check if copying data is needed*/
        ptr -= MEM_BLOCK_SIZE_B;
        pBlockAddr = ptr;
        eeprom_read_block(&pBlock, (uint16_t*)pBlockAddr, MEM_BLOCK_SIZE_B);
		    i = pBlock.blockSize;

        ptr += MEM_BLOCK_SIZE_B + pBlock.blockSize;
        pBlockAddr = ptr;
        eeprom_read_block(&pBlock, (uint16_t*)pBlockAddr, MEM_BLOCK_SIZE_B);

        if ((pBlock.pNextFreeBlock == StartAddress) || (i + pBlock.blockSize + MEM_BLOCK_SIZE_B < requestedSize)) {
			       needToCopy = 'Y';
		    }else {
			       needToCopy = 'N';
		    }

        /*If copying data is not needed*/
		    if (needToCopy == 'N') {

          /*load actual block*/
          ptr = ptrToRealloc;
          ptr -= MEM_BLOCK_SIZE_B;
          pBlockAddr = ptr;
          eeprom_read_block(&pBlock, (uint16_t*)pBlockAddr, MEM_BLOCK_SIZE_B);

          /* load next block*/
          ptr += MEM_BLOCK_SIZE_B + pBlock.blockSize;
          pNextAddr = ptr;
			    eeprom_read_block(&pNextBlock, (uint16_t*)pNextAddr, MEM_BLOCK_SIZE_B);

          /*load next to new block*/
          ptr += MEM_BLOCK_SIZE_B + pNextBlock.blockSize;
          pNextToNewAddr = ptr;
          eeprom_read_block(&pNextToNewBlock, (uint16_t*)pNextToNewAddr, MEM_BLOCK_SIZE_B);

          /*If new block will not be created. New size matches size of actual block and size of next free block*/
          if (i + pBlock.blockSize + MEM_BLOCK_SIZE_B == requestedSize) {
              i = pNextBlock.blockSize;
              deleteFromList(pNextAddr, pNextBlock);

              pBlock.blockSize += i + MEM_BLOCK_SIZE_B;
              eeprom_write_block(&pBlock, (uint16_t*)pBlockAddr, MEM_BLOCK_SIZE_B);

              pNextToNewBlock.pPrevBlock = pBlockAddr;
              eeprom_write_block(&pNextToNewBlock, (uint16_t*)pNextToNewAddr, MEM_BLOCK_SIZE_B);

              toReturn = pBlockAddr + MEM_BLOCK_SIZE_B;

              actFreeMem -= i;
          }
          /*New block will be created*/
          else {
              ptr = ptrToRealloc;
              ptr += requestedSize;
              pNewAddr = ptr;
              eeprom_read_block(&pNewBlock, (uint16_t*)pNewAddr, MEM_BLOCK_SIZE_B);

              i = pNextBlock.blockSize;
				      deleteFromList(pNextAddr, pNextBlock);

              pNewBlock.pPrevBlock = pBlockAddr;
				      pNewBlock.blockSize = i - (requestedSize - pBlock.blockSize);
              eeprom_write_block(&pNewBlock, (uint16_t*)pNewAddr, MEM_BLOCK_SIZE_B);
				      actFreeMem -= requestedSize - pBlock.blockSize;

              pNextToNewBlock.pPrevBlock = pBlockAddr;
              eeprom_write_block(&pNextToNewBlock, (uint16_t*)pNextToNewAddr, MEM_BLOCK_SIZE_B);

              pBlock.blockSize = requestedSize;
              eeprom_write_block(&pBlock, (uint16_t*)pBlockAddr, MEM_BLOCK_SIZE_B);

              insertNewBlock(pNewAddr, pNewBlock);

              toReturn = pBlockAddr + MEM_BLOCK_SIZE_B;

          }

        }


		    /*If it is needed to copy data*/
		    if (needToCopy == 'Y') {
            /* Allocate new block of memory */
            toReturn = bMemAlloc(requestedSize);

            /* Copy data if allocation was successfull */
      			if (toReturn != NONE) {
              ptr = ptrToRealloc;
              ptr -= MEM_BLOCK_SIZE_B;
              pBlockAddr = ptr;
              eeprom_read_block(&pBlock, (uint16_t*)pBlockAddr, MEM_BLOCK_SIZE_B);

              /*Set pointers to copying*/
  				    pNewAddr = toReturn;
  				    ptr += MEM_BLOCK_SIZE_B;

              if (requestedSize >= pBlock.blockSize) {
  					     for (i = 0; i < pBlock.blockSize; i++) {
                    uint8_t pom = eeprom_read_byte((uint8_t*)(ptr + i));
                    eeprom_write_byte((uint8_t*)(pNewAddr + i), pom);
  					     }
  				    }

              if (requestedSize < pBlock.blockSize) {
					       for (i = 0; i < requestedSize; i++) {
                   uint8_t pom = eeprom_read_byte((uint8_t*)(ptr + i));
                   eeprom_write_byte((uint8_t*)(pNewAddr + i), pom);
					       }
				      }

        				/* Make old pointer free*/
        				bMemFree(ptrToRealloc);
            }
        }
    }

    return (uint16_t)toReturn;

}


void bMemFree(uint16_t ptrToFree){
  uint16_t blockAddr;
  uint16_t nextAddr;
  uint16_t ptr = ptrToFree;
  Mem_block block, next;

  if(ptrToFree < EEPROM){
    /*Jump on the beginning of the block*/
		ptr -= MEM_BLOCK_SIZE_B;

    /*Cast to Mem_block type*/
    blockAddr = ptr;
    eeprom_read_block(&block, (uint16_t*)blockAddr, MEM_BLOCK_SIZE_B);

    insertNewBlock(blockAddr, block);
    eeprom_read_block(&block, (uint16_t*)blockAddr, MEM_BLOCK_SIZE_B);


    /* Increase free memory*/
    actFreeMem += block.blockSize;

    /*Try to join right next block*/
		ptr = blockAddr;
		ptr += MEM_BLOCK_SIZE_B + block.blockSize;
		nextAddr = ptr;
    eeprom_read_block(&next, (uint16_t*)nextAddr, MEM_BLOCK_SIZE_B);

		if (next.pNextFreeBlock != StartAddress && nextAddr != EndAddress) {
			joinBlock(blockAddr, block);
		}

    next = block;
    nextAddr = blockAddr;

		blockAddr = block.pPrevBlock;
    eeprom_read_block(&block, (uint16_t*)blockAddr, MEM_BLOCK_SIZE_B);

		/*Try to join left*/
		if (blockAddr != StartAddress && block.pNextFreeBlock != StartAddress) {
			joinBlock(blockAddr, block);
		}

  }


}



/* ********* PRIVATE FUNCTIONS **************** */


static void insertNewBlock(uint16_t newAddr, Mem_block pNewBlockToInsert){
    uint16_t itrAddr = StartAddress;
    uint16_t prevAddr;
    Mem_block blockItr, blockPrev;

    eeprom_read_block(&blockItr, (uint16_t*)itrAddr, MEM_BLOCK_SIZE_B);
    		/*Find the right place in list for block to be inserted*/
		while (1) {

  			if (blockItr.blockSize >= pNewBlockToInsert.blockSize) {
  				break;
  			}
  			blockPrev = blockItr;
        prevAddr = itrAddr;

        itrAddr = blockItr.pNextFreeBlock;
        eeprom_read_block(&blockItr, (uint16_t*)itrAddr, MEM_BLOCK_SIZE_B);

		}

		/*Insert block*/
		blockPrev.pNextFreeBlock = newAddr;
    eeprom_write_block(&blockPrev, (uint16_t*)prevAddr, MEM_BLOCK_SIZE_B);


		pNewBlockToInsert.pNextFreeBlock = itrAddr;
    eeprom_write_block(&pNewBlockToInsert, (uint16_t*)newAddr, MEM_BLOCK_SIZE_B);

}


static void joinBlock(uint16_t blockAddr, Mem_block block){
    Mem_block nextBlock;
    uint16_t nextAddr;
    uint16_t ptr;

  /*Get next physical block*/
  ptr = blockAddr;
  ptr += MEM_BLOCK_SIZE_B + block.blockSize;
  nextAddr = ptr;
  eeprom_read_block(&nextBlock, (uint16_t*)nextAddr, MEM_BLOCK_SIZE_B);


  deleteFromList(blockAddr, block);
  eeprom_read_block(&block, (uint16_t*)blockAddr, MEM_BLOCK_SIZE_B);

  eeprom_read_block(&nextBlock, (uint16_t*)nextAddr, MEM_BLOCK_SIZE_B);
	deleteFromList(nextAddr, nextBlock);
  eeprom_read_block(&nextBlock, (uint16_t*)nextAddr, MEM_BLOCK_SIZE_B);


	actFreeMem -= block.blockSize;
	actFreeMem -= nextBlock.blockSize;

  /*Make actual block bigger*/
	block.blockSize += MEM_BLOCK_SIZE_B + nextBlock.blockSize;
  eeprom_write_block(&block, (uint16_t*)blockAddr, MEM_BLOCK_SIZE_B);

  /*Delete next block*/
	ptr = nextAddr;
	ptr += MEM_BLOCK_SIZE_B + nextBlock.blockSize;
	nextAddr = ptr;
  eeprom_read_block(&nextBlock, (uint16_t*)nextAddr, MEM_BLOCK_SIZE_B);

  nextBlock.pPrevBlock = blockAddr;
  eeprom_write_block(&nextBlock, (uint16_t*)nextAddr, MEM_BLOCK_SIZE_B);

  /*Insert new block*/
	insertNewBlock(blockAddr, block);
	actFreeMem += block.blockSize;

}

/*
* Deletes block from linked list of free blocks. List stay oredered
*
* @param toDel Block which will be deleted from linked list
*/
static void deleteFromList(uint16_t toDelAddr, Mem_block toDelBlock){
    uint16_t itrAddr, prevAddr;
    Mem_block itrBlock, prevBlock;

    itrAddr = StartAddress;
    eeprom_read_block(&itrBlock, (uint16_t*)itrAddr, MEM_BLOCK_SIZE_B);

    if(toDelAddr < EEPROM){
        /*Find place in list where toDel is stored*/
        while(1){

            if(itrAddr == toDelAddr){
              break;
            }
            prevAddr = itrAddr;
            itrAddr = itrBlock.pNextFreeBlock;
            eeprom_read_block(&itrBlock, (uint16_t*)itrAddr, MEM_BLOCK_SIZE_B);

        }
        /*Delete block*/
        eeprom_read_block(&prevBlock, (uint16_t*)prevAddr, MEM_BLOCK_SIZE_B);
		    prevBlock.pNextFreeBlock = toDelBlock.pNextFreeBlock;
        eeprom_write_block(&prevBlock, (uint16_t*)prevAddr, MEM_BLOCK_SIZE_B);


    }

}


static void clearMem(){
  uint16_t i = 0;
  for(i=0; i<EEPROM; i++){
    eeprom_write_byte((uint8_t*)i, 0);
  }
}





/* *********    PRINT FUNCTIONS   *********** */

static void bPrintOneStruct(Mem_block block){
  Serial.println("One block");
  Serial.print("Next free block: ");Serial.println(block.pNextFreeBlock);
  Serial.print("Previous block: ");Serial.println(block.pPrevBlock);
  Serial.print("Block size: ");Serial.println(block.blockSize);
}




void bPrintLinkedList() {
	Mem_block block;
  uint16_t pAct = StartAddress;

  Serial.println("List of free memory block");
  Serial.print("Size of block: ");Serial.println(MEM_BLOCK_SIZE_B);

	/*Iterates whole list and prints size of each block from Start to penultimate block*/
  eeprom_read_block(&block, (uint16_t*)pAct, MEM_BLOCK_SIZE_B);
  Serial.print("First block: ");Serial.print(block.blockSize);Serial.println(" START");

  while(1){
      pAct = block.pNextFreeBlock;
      eeprom_read_block(&block, (uint16_t*)pAct, MEM_BLOCK_SIZE_B);
      if(block.pNextFreeBlock == NONE){
        break;
      }
      Serial.print("Free block: ");Serial.println(block.blockSize);

  }

	/*Prints size of End block*/
  Serial.print("Last block: ");Serial.print(block.blockSize);Serial.println(" END");

	/*Prints real actual free memory */
	Serial.print("Remaining free memory: ");Serial.println(actFreeMem);

}


void bPrintWholeMemory(){
  Mem_block block;
  uint16_t pAct = StartAddress;

  Serial.println("List of all blocks of memory");

  eeprom_read_block(&block, (uint16_t*)pAct, MEM_BLOCK_SIZE_B);
  Serial.print("Block    addr: ");Serial.print(pAct);Serial.print("     size: ");Serial.print(block.blockSize);Serial.println("     START");

  while (1) {
		pAct += (MEM_BLOCK_SIZE_B + block.blockSize);
		eeprom_read_block(&block, (uint16_t*)pAct, MEM_BLOCK_SIZE_B);

		if (block.blockSize == EEPROM) {
			break;
		}

		if (block.pNextFreeBlock == StartAddress) {
      Serial.print("Block    addr: ");Serial.print(pAct+MEM_BLOCK_SIZE_B);Serial.print("     size: ");Serial.print(block.blockSize);Serial.println("      ALLOCATED");
		}
		else {
			Serial.print("Block    addr: ");Serial.print(pAct+MEM_BLOCK_SIZE_B);Serial.print("     size: ");Serial.print(block.blockSize);Serial.println("     FREE");
		}

	}

	Serial.print("Block    addr: ");Serial.print(pAct);Serial.print("     size: ");Serial.print(block.blockSize);Serial.println("      END");
	Serial.print("Remaining free memory: ");Serial.println(actFreeMem);

}


void bPrintWholeMemoryReverse(){
    Mem_block block;
    uint16_t actAdd = EndAddress;

    Serial.println("Reverse list of all blocks");

    eeprom_read_block(&block, (uint16_t*)actAdd, MEM_BLOCK_SIZE_B);
    Serial.print("Block ");Serial.print(block.blockSize);Serial.println(" END");

    while(1){
      actAdd = block.pPrevBlock;
      eeprom_read_block(&block, (uint16_t*)actAdd, MEM_BLOCK_SIZE_B);
      if(block.blockSize == 0){break;}

      if (block.pNextFreeBlock == StartAddress) {
			     Serial.print("Block ");Serial.print(block.blockSize);Serial.println(" ALLOCATED");
		  }
		  else {
			    Serial.print("Block ");Serial.print(block.blockSize);Serial.println(" FREE");
		  }

    }

    Serial.print("Block ");Serial.print(block.blockSize);Serial.println(" START");
}


uint16_t getBlockSize(uint16_t ptr){
  Mem_block block;
  ptr -= MEM_BLOCK_SIZE_B;
  eeprom_read_block(&block, (uint16_t*)ptr, MEM_BLOCK_SIZE_B);
  return block.blockSize;
}
