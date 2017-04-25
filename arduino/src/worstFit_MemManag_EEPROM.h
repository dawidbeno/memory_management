
#include <Arduino.h>
#include <stdint.h>
#include <avr/eeprom.h>


/*
* There are three pools of memory in the microcontroller used on avr-based Arduino boards :
*
* Flash memory - is where Arduino sketch is stored
* SRAM (static random access memory) - sketch creates and manipulates variables here
* EEPROM - programmer can store long-term information here
*
* Flash and EEPROM are non-volatile(the information persists after the power is turned off),
* SRAM is volatile and will be lost when the power is cycled.
*/

/*
* Arduino mega 2560 memory space -- this information might be pulled from some config file
*/
#define W_FLASH_MEM ((1024 * sizeof(char))*(256-8)) // 8k is used for bootloader
#define W_SRAM ((1024 * sizeof(char)) * 8)
#define W_EEPROM ((1024 * sizeof(char)) * 4)

/*
Defined structure for linked list, where are all blocks stored
*/
typedef struct W_MEM_BLOCK
{
	uint16_t pNextFreeBlock; // pointer to next free block in list of free blocks
	uint16_t pPrevBlock;  // previous physical memory block
	uint16_t blockSize; // size of actual block
} wMem_block;



/*
* Size of memory block used by this allocator
*/
#define MEM_BLOCK_SIZE_W sizeof(wMem_block)

#define W_NONE 9999




/*
* Prepares data structure Linked list, where blocks are stored
* Must be called before using bMemAlloc function.
* @params
*/
void wMemInit();


/*
* Allocates memory block and returns pointer to memory space
*
* @param requestedSize Amount of memory to be allocated and accessible from returned pointer
*/
uint16_t wMemAlloc(unsigned int requestedSize);


/*
* Pointer that was used will be set free and inserted to the right place in the linked list
* of free memory blocks, so list stays sorted
*
@param ptrToFree Pointer to memory which will be set free
*/
int wMemFree(uint16_t ptrToFree);


/*
* Pointer has assigned some amount of memory. Use this function to change memory space
* assigned to pointer. Memory space can be either increased or decreased
*
* @param ptrToRealloc The pointer to memory space which will be reallocated
*
* @param requestedSize New amount of memory which will be assigned to ptrToRealloc
*/
uint16_t wMemRealloc(uint16_t ptrToRealloc, uint16_t requestedSize);


/*
 Prints actual whole linked list of memory blocks
*/
void wPrintLinkedList();


/*
* Print whole memory blocks
*/
void wPrintWholeMemory();

/*
* Print whole physical memory reverse
* This print is based on iterating through pointers which point to previous memory block
* Starts at the End and iterates to the Start
*/
void wPrintWholeMemoryReverse();


uint16_t wgetBlockSize(uint16_t ptr);

uint16_t wgetRemainingMem();
