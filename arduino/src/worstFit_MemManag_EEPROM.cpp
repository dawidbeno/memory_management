
#include "worstFit_MemManag_EEPROM.h"

uint16_t WStartAddress = 0;
uint16_t WEndAddress = W_EEPROM - MEM_BLOCK_SIZE_W;


/*
Actual free memory
*/
uint16_t WactFreeMem = W_EEPROM - (2*MEM_BLOCK_SIZE_W); // 2 * MEM_BLOCK_SIZE

static void winsertNewBlock(uint16_t newAddr, wMem_block pNewBlockToInsert);
static void wjoinBlock(uint16_t blockAddr, wMem_block block);
static void wdeleteFromList(uint16_t toDelAddr, wMem_block toDelBlock);
static void wclearMem();


void wMemInit(){
  //wclearMem();
  wMem_block block;
  uint16_t ptr = WStartAddress;

  WactFreeMem = W_EEPROM - (2*MEM_BLOCK_SIZE_W);

  /*Initialises start of linked list*/
  block.pNextFreeBlock = WStartAddress + MEM_BLOCK_SIZE_W;
	block.pPrevBlock = W_NONE;
	block.blockSize = W_EEPROM;
  eeprom_write_block(&block, (uint16_t*)ptr, MEM_BLOCK_SIZE_W);

  /*shift pointer*/
	ptr += MEM_BLOCK_SIZE_W;

  /* New block represents whole free memory, insert between pStart and pEnd */
  block.pNextFreeBlock = WEndAddress;  //points to END
  block.pPrevBlock = WStartAddress;
  block.blockSize = WactFreeMem - MEM_BLOCK_SIZE_W;
  eeprom_write_block(&block, (uint16_t*)ptr, MEM_BLOCK_SIZE_W);

  /*shift pointer*/
  ptr += (MEM_BLOCK_SIZE_W + block.blockSize);

  block.pNextFreeBlock = W_NONE;
  block.pPrevBlock = (WStartAddress + MEM_BLOCK_SIZE_W);
  block.blockSize = 0;
  eeprom_write_block(&block, (uint16_t*)ptr, MEM_BLOCK_SIZE_W);

  WactFreeMem -= MEM_BLOCK_SIZE_W;

}


uint16_t wMemAlloc(uint16_t requestedSize){
    uint16_t ptr = WStartAddress;
    uint16_t toReturn = W_NONE;
    wMem_block pPrev, pAct, pNew;
    uint16_t actAddr;
    uint16_t prevAddr;
    uint16_t newAddr;

    /* Cannot allocate 0 bytes*/
	if (requestedSize <= 0) {
		return W_NONE;
	}

  /*For better computing -- this condition can be deleted*/
	if (requestedSize % 2 != 0) {
		requestedSize++;
	}

  /*If requested size is still lower than actual free space in memory*/
  	if (requestedSize <= WactFreeMem) {

      /*We allocate memory for request and for new block*/
      requestedSize += MEM_BLOCK_SIZE_W;

      prevAddr = ptr;
      eeprom_read_block(&pPrev, (uint16_t*)ptr, MEM_BLOCK_SIZE_W);

      actAddr = pPrev.pNextFreeBlock;
      eeprom_read_block(&pAct, (uint16_t*)pPrev.pNextFreeBlock, MEM_BLOCK_SIZE_W);


      /*Found free block. Block size and requested size matches*/
  		if (pAct.pNextFreeBlock != W_NONE && (pAct.blockSize == (requestedSize - MEM_BLOCK_SIZE_W) || pAct.blockSize == requestedSize)) {

        toReturn = actAddr + MEM_BLOCK_SIZE_W;  // pointer to block which will be returned

        pPrev.pNextFreeBlock = pAct.pNextFreeBlock; // actual block is deleted from list of free blocks
        eeprom_write_block(&pPrev, (uint16_t*)prevAddr, MEM_BLOCK_SIZE_W);

        WactFreeMem -= (requestedSize - MEM_BLOCK_SIZE_W);	 // actual free memory is decreased

        pAct.pNextFreeBlock = WStartAddress;
        eeprom_write_block(&pAct, (uint16_t*)actAddr, MEM_BLOCK_SIZE_W);

  		}

        /*Found free block. Requested size is bigger than blocksize of actual block.
  		New block will be created and insert to linked list of free blocks.*/
  		if (pAct.pNextFreeBlock != W_NONE && pAct.blockSize > requestedSize) {

        /*requestedSize = request + size of BLOCK, because pointer must jump over actual block and requested size of memory.
  			It ends on the begginig of new block*/
  			newAddr = actAddr + requestedSize;

        /*Actual free memory space is decreased
  			Space for new block is counted in requestedSize*/
  			WactFreeMem -= requestedSize;

        /*New block is filled with its data*/
  			pNew.blockSize = pAct.blockSize - requestedSize;
  			pNew.pNextFreeBlock = W_NONE;
  			pNew.pPrevBlock = actAddr;

        /*Update of actual block*/
  			pAct.blockSize = requestedSize - (MEM_BLOCK_SIZE_W);

        /*actual block is deleted from list of free blocks*/
  			pPrev.pNextFreeBlock = pAct.pNextFreeBlock;
        eeprom_write_block(&pPrev, (uint16_t*)prevAddr, MEM_BLOCK_SIZE_W);

        /*Insert new block to linked list of free blocks*/
  			winsertNewBlock(newAddr, pNew);

        /*pointer to block which will be returned*/
  			toReturn = actAddr + MEM_BLOCK_SIZE_W;

        /*Set pPrevBlock to the next block - set to actual block*/
  			ptr = newAddr;
  			ptr += MEM_BLOCK_SIZE_W + pNew.blockSize;
        eeprom_read_block(&pPrev, (uint16_t*)ptr, MEM_BLOCK_SIZE_W);
  			pPrev.pPrevBlock = newAddr;
        eeprom_write_block(&pPrev, (uint16_t*)ptr, MEM_BLOCK_SIZE_W);

        /*allocated block points to the Start of memory*/
        pAct.pNextFreeBlock = WStartAddress;
        eeprom_write_block(&pAct, (uint16_t*)actAddr, MEM_BLOCK_SIZE_W);

        }


    }

  return (uint16_t)toReturn;

}



int wMemFree(uint16_t ptrToFree){
  uint16_t blockAddr;
  uint16_t nextAddr;
  uint16_t ptr = ptrToFree;
  int numOfJoins = 0;
  wMem_block block, next;

  if(ptrToFree < W_EEPROM){
    /*Jump on the beginning of the block*/
		ptr -= MEM_BLOCK_SIZE_W;

    /*Cast to Mem_block type*/
    blockAddr = ptr;
    eeprom_read_block(&block, (uint16_t*)blockAddr, MEM_BLOCK_SIZE_W);

    winsertNewBlock(blockAddr, block);
    eeprom_read_block(&block, (uint16_t*)blockAddr, MEM_BLOCK_SIZE_W);


    /* Increase free memory*/
    WactFreeMem += block.blockSize;

    /*Try to join right next block*/
		ptr = blockAddr;
		ptr += MEM_BLOCK_SIZE_W + block.blockSize;
		nextAddr = ptr;
    eeprom_read_block(&next, (uint16_t*)nextAddr, MEM_BLOCK_SIZE_W);

		if (next.pNextFreeBlock != WStartAddress && nextAddr != WEndAddress) {
			wjoinBlock(blockAddr, block);
      numOfJoins++;
		}

    next = block;
    nextAddr = blockAddr;

		blockAddr = block.pPrevBlock;
    eeprom_read_block(&block, (uint16_t*)blockAddr, MEM_BLOCK_SIZE_W);

		/*Try to join left*/
		if (blockAddr != WStartAddress && block.pNextFreeBlock != WStartAddress) {
			wjoinBlock(blockAddr, block);
      numOfJoins++;
		}

  }

return numOfJoins;
}


uint16_t wMemRealloc(uint16_t ptrToRealloc, uint16_t requestedSize){
    uint16_t toReturn;
    wMem_block pBlock, pNextBlock, pNewBlock, pNextToNewBlock;
    uint16_t pBlockAddr, pNextAddr, pNewAddr, pNextToNewAddr;
    uint16_t ptr = ptrToRealloc;
    uint16_t i;
    char needToCopy = 'N';

    if (requestedSize <= 0) {
		    return W_NONE;
	  }

    if(ptrToRealloc < W_EEPROM){
        /*First check if copying data is needed*/
        ptr -= MEM_BLOCK_SIZE_W;
        pBlockAddr = ptr;
        eeprom_read_block(&pBlock, (uint16_t*)pBlockAddr, MEM_BLOCK_SIZE_W);
		    i = pBlock.blockSize;

        ptr += MEM_BLOCK_SIZE_W + pBlock.blockSize;
        pBlockAddr = ptr;
        eeprom_read_block(&pBlock, (uint16_t*)pBlockAddr, MEM_BLOCK_SIZE_W);

        if ((pBlock.pNextFreeBlock == WStartAddress) || (i + pBlock.blockSize + MEM_BLOCK_SIZE_W < requestedSize)) {
			       needToCopy = 'Y';
		    }else {
			       needToCopy = 'N';
		    }

        /*If copying data is not needed*/
		    if (needToCopy == 'N') {

          /*load actual block*/
          ptr = ptrToRealloc;
          ptr -= MEM_BLOCK_SIZE_W;
          pBlockAddr = ptr;
          eeprom_read_block(&pBlock, (uint16_t*)pBlockAddr, MEM_BLOCK_SIZE_W);

          /* load next block*/
          ptr += MEM_BLOCK_SIZE_W + pBlock.blockSize;
          pNextAddr = ptr;
			    eeprom_read_block(&pNextBlock, (uint16_t*)pNextAddr, MEM_BLOCK_SIZE_W);

          /*load next to new block*/
          ptr += MEM_BLOCK_SIZE_W + pNextBlock.blockSize;
          pNextToNewAddr = ptr;
          eeprom_read_block(&pNextToNewBlock, (uint16_t*)pNextToNewAddr, MEM_BLOCK_SIZE_W);

          /*If new block will not be created. New size matches size of actual block and size of next free block*/
          if (i + pBlock.blockSize + MEM_BLOCK_SIZE_W == requestedSize) {
              i = pNextBlock.blockSize;
              wdeleteFromList(pNextAddr, pNextBlock);

              pBlock.blockSize += i + MEM_BLOCK_SIZE_W;
              eeprom_write_block(&pBlock, (uint16_t*)pBlockAddr, MEM_BLOCK_SIZE_W);

              pNextToNewBlock.pPrevBlock = pBlockAddr;
              eeprom_write_block(&pNextToNewBlock, (uint16_t*)pNextToNewAddr, MEM_BLOCK_SIZE_W);

              toReturn = pBlockAddr + MEM_BLOCK_SIZE_W;

              WactFreeMem -= i;
          }
          /*New block will be created*/
          else {
              ptr = ptrToRealloc;
              ptr += requestedSize;
              pNewAddr = ptr;
              eeprom_read_block(&pNewBlock, (uint16_t*)pNewAddr, MEM_BLOCK_SIZE_W);

              i = pNextBlock.blockSize;
				      wdeleteFromList(pNextAddr, pNextBlock);

              pNewBlock.pPrevBlock = pBlockAddr;
				      pNewBlock.blockSize = i - (requestedSize - pBlock.blockSize);
              eeprom_write_block(&pNewBlock, (uint16_t*)pNewAddr, MEM_BLOCK_SIZE_W);
				      WactFreeMem -= requestedSize - pBlock.blockSize;

              pNextToNewBlock.pPrevBlock = pBlockAddr;
              eeprom_write_block(&pNextToNewBlock, (uint16_t*)pNextToNewAddr, MEM_BLOCK_SIZE_W);

              pBlock.blockSize = requestedSize;
              eeprom_write_block(&pBlock, (uint16_t*)pBlockAddr, MEM_BLOCK_SIZE_W);

              winsertNewBlock(pNewAddr, pNewBlock);

              toReturn = pBlockAddr + MEM_BLOCK_SIZE_W;

          }

        }


		    /*If it is needed to copy data*/
		    if (needToCopy == 'Y') {
            /* Allocate new block of memory */
            toReturn = wMemAlloc(requestedSize);

            /* Copy data if allocation was successfull */
      			if (toReturn != W_NONE) {
              ptr = ptrToRealloc;
              ptr -= MEM_BLOCK_SIZE_W;
              pBlockAddr = ptr;
              eeprom_read_block(&pBlock, (uint16_t*)pBlockAddr, MEM_BLOCK_SIZE_W);

              /*Set pointers to copying*/
  				    pNewAddr = toReturn;
  				    ptr += MEM_BLOCK_SIZE_W;

              if (requestedSize >= pBlock.blockSize) {
  					     for (i = 0; i < pBlock.blockSize; i++) {
                    uint8_t pom = eeprom_read_byte((uint8_t*)(ptr + i));
                    eeprom_write_byte((uint8_t*)(pNewAddr + i), pom);
                    //Serial.println("copy");
  					     }
  				    }

              if (requestedSize < pBlock.blockSize) {
					       for (i = 0; i < requestedSize; i++) {
                   uint8_t pom = eeprom_read_byte((uint8_t*)(ptr + i));
                   eeprom_write_byte((uint8_t*)(pNewAddr + i), pom);
					       }
				      }

        				/* Make old pointer free*/
        				wMemFree(ptrToRealloc);
            }
        }
    }

    return (uint16_t)toReturn;

}






/* ********* PRIVATE FUNCTIONS **************** */


static void winsertNewBlock(uint16_t newAddr, wMem_block pNewBlockToInsert){
    uint16_t itrAddr = WStartAddress;
    uint16_t prevAddr;
    wMem_block blockItr, blockPrev;

    eeprom_read_block(&blockItr, (uint16_t*)itrAddr, MEM_BLOCK_SIZE_W);
    		/*Find the right place in list for block to be inserted*/
		while (1) {
        Serial.println("Inserting block");
  			if (blockItr.blockSize <= pNewBlockToInsert.blockSize) {
  				break;
  			}
  			blockPrev = blockItr;
        prevAddr = itrAddr;

        itrAddr = blockItr.pNextFreeBlock;
        eeprom_read_block(&blockItr, (uint16_t*)itrAddr, MEM_BLOCK_SIZE_W);

		}

		/*Insert block*/
		blockPrev.pNextFreeBlock = newAddr;
    eeprom_write_block(&blockPrev, (uint16_t*)prevAddr, MEM_BLOCK_SIZE_W);


		pNewBlockToInsert.pNextFreeBlock = itrAddr;
    eeprom_write_block(&pNewBlockToInsert, (uint16_t*)newAddr, MEM_BLOCK_SIZE_W);

}



static void wjoinBlock(uint16_t blockAddr, wMem_block block){
    wMem_block nextBlock;
    uint16_t nextAddr;
    uint16_t ptr;

  /*Get next physical block*/
  ptr = blockAddr;
  ptr += MEM_BLOCK_SIZE_W + block.blockSize;
  nextAddr = ptr;
  eeprom_read_block(&nextBlock, (uint16_t*)nextAddr, MEM_BLOCK_SIZE_W);


  wdeleteFromList(blockAddr, block);
  eeprom_read_block(&block, (uint16_t*)blockAddr, MEM_BLOCK_SIZE_W);

  eeprom_read_block(&nextBlock, (uint16_t*)nextAddr, MEM_BLOCK_SIZE_W);
	wdeleteFromList(nextAddr, nextBlock);
  eeprom_read_block(&nextBlock, (uint16_t*)nextAddr, MEM_BLOCK_SIZE_W);


	WactFreeMem -= block.blockSize;
	WactFreeMem -= nextBlock.blockSize;

  /*Make actual block bigger*/
	block.blockSize += MEM_BLOCK_SIZE_W + nextBlock.blockSize;
  eeprom_write_block(&block, (uint16_t*)blockAddr, MEM_BLOCK_SIZE_W);

  /*Delete next block*/
	ptr = nextAddr;
	ptr += MEM_BLOCK_SIZE_W + nextBlock.blockSize;
	nextAddr = ptr;
  eeprom_read_block(&nextBlock, (uint16_t*)nextAddr, MEM_BLOCK_SIZE_W);

  nextBlock.pPrevBlock = blockAddr;
  eeprom_write_block(&nextBlock, (uint16_t*)nextAddr, MEM_BLOCK_SIZE_W);

  /*Insert new block*/
	winsertNewBlock(blockAddr, block);
	WactFreeMem += block.blockSize;

}


/*
* Deletes block from linked list of free blocks. List stay oredered
*
* @param toDel Block which will be deleted from linked list
*/
static void wdeleteFromList(uint16_t toDelAddr, wMem_block toDelBlock){
    uint16_t itrAddr, prevAddr;
    wMem_block itrBlock, prevBlock;

    itrAddr = WStartAddress;
    eeprom_read_block(&itrBlock, (uint16_t*)itrAddr, MEM_BLOCK_SIZE_W);

    if(toDelAddr < W_EEPROM){
        /*Find place in list where toDel is stored*/
        while(1){

            if(itrAddr == toDelAddr){
              break;
            }
            prevAddr = itrAddr;
            itrAddr = itrBlock.pNextFreeBlock;
            eeprom_read_block(&itrBlock, (uint16_t*)itrAddr, MEM_BLOCK_SIZE_W);

        }
        /*Delete block*/
        eeprom_read_block(&prevBlock, (uint16_t*)prevAddr, MEM_BLOCK_SIZE_W);
		    prevBlock.pNextFreeBlock = toDelBlock.pNextFreeBlock;
        eeprom_write_block(&prevBlock, (uint16_t*)prevAddr, MEM_BLOCK_SIZE_W);


    }

}


static void wclearMem(){
  uint16_t i = 0;
  for(i=0; i<W_EEPROM; i++){
    eeprom_write_byte((uint8_t*)i, 0);
  }
}

uint16_t wgetRemainingMem(){
  return WactFreeMem;
}



/* *********    PRINT FUNCTIONS   *********** */

static void wPrintOneStruct(wMem_block block){
  Serial.println("One block");
  Serial.print("Next free block: ");Serial.println(block.pNextFreeBlock);
  Serial.print("Previous block: ");Serial.println(block.pPrevBlock);
  Serial.print("Block size: ");Serial.println(block.blockSize);
}




void wPrintLinkedList() {
	wMem_block block;
  uint16_t pAct = WStartAddress;

  Serial.println("List of free memory block");
  Serial.print("Size of block: ");Serial.println(MEM_BLOCK_SIZE_W);

	/*Iterates whole list and prints size of each block from Start to penultimate block*/
  eeprom_read_block(&block, (uint16_t*)pAct, MEM_BLOCK_SIZE_W);
  Serial.print("First block: ");Serial.print(block.blockSize);Serial.println(" START");

  while(1){
      pAct = block.pNextFreeBlock;
      eeprom_read_block(&block, (uint16_t*)pAct, MEM_BLOCK_SIZE_W);
      if(block.pNextFreeBlock == W_NONE){
        break;
      }
      Serial.print("Free block: ");Serial.println(block.blockSize);

  }

	/*Prints size of End block*/
  Serial.print("Last block: ");Serial.print(block.blockSize);Serial.println(" END");

	/*Prints real actual free memory */
	Serial.print("Remaining free memory: ");Serial.println(WactFreeMem);

}


void wPrintWholeMemory(){
  wMem_block block;
  uint16_t pAct = WStartAddress;

  Serial.println("List of all blocks of memory");

  eeprom_read_block(&block, (uint16_t*)pAct, MEM_BLOCK_SIZE_W);
  Serial.print("Block    addr: ");Serial.print(pAct);Serial.print("     size: ");Serial.print(block.blockSize);Serial.println("     START");

  pAct += MEM_BLOCK_SIZE_W;
  eeprom_read_block(&block, (uint16_t*)pAct, MEM_BLOCK_SIZE_W);

  while (1) {
		if (block.blockSize == 0) {
			break;
		}

		if (block.pNextFreeBlock == WStartAddress) {
      Serial.print("Block    addr: ");Serial.print(pAct+MEM_BLOCK_SIZE_W);Serial.print("     size: ");Serial.print(block.blockSize);Serial.println("      ALLOCATED");
		}
		else {
			Serial.print("Block    addr: ");Serial.print(pAct+MEM_BLOCK_SIZE_W);Serial.print("     size: ");Serial.print(block.blockSize);Serial.println("     FREE");
		}

    pAct += (MEM_BLOCK_SIZE_W + block.blockSize);
    eeprom_read_block(&block, (uint16_t*)pAct, MEM_BLOCK_SIZE_W);

	}

	Serial.print("Block    addr: ");Serial.print(pAct);Serial.print("     size: ");Serial.print(block.blockSize);Serial.println("      END");
	Serial.print("Remaining free memory: ");Serial.println(WactFreeMem);

}


void wPrintWholeMemoryReverse(){
    wMem_block block;
    uint16_t actAdd = WEndAddress;

    Serial.println("Reverse list of all blocks");

    eeprom_read_block(&block, (uint16_t*)actAdd, MEM_BLOCK_SIZE_W);
    Serial.print("Block ");Serial.print(block.blockSize);Serial.println(" END");

    while(1){
      actAdd = block.pPrevBlock;
      eeprom_read_block(&block, (uint16_t*)actAdd, MEM_BLOCK_SIZE_W);
      if(block.blockSize == 0){break;}

      if (block.pNextFreeBlock == WStartAddress) {
			     Serial.print("Block ");Serial.print(block.blockSize);Serial.println(" ALLOCATED");
		  }
		  else {
			    Serial.print("Block ");Serial.print(block.blockSize);Serial.println(" FREE");
		  }

    }

    Serial.print("Block ");Serial.print(block.blockSize);Serial.println(" START");
}


uint16_t wgetBlockSize(uint16_t ptr){
  wMem_block block;
  ptr -= MEM_BLOCK_SIZE_W;
  eeprom_read_block(&block, (uint16_t*)ptr, MEM_BLOCK_SIZE_W);
  return block.blockSize;
}
