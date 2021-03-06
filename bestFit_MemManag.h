#pragma once

#ifndef B_MEM_BEST_FIT_H
#define B_MEM_BEST_FIT_H

/*
Different int types can be used

C type 						stdint.h type	 Bits		Sign				Range
----------------------------------------------------------------------------------------------------------
char 								= uint8_t  - 8 		- unsigned 		- 0..255
signed char 				=	int8_t	 - 8		- Signed			-128 .. 127
unsigned short			= uint16_t - 16		- Unsigned		0 .. 65,535
short	 							=	int16_t  - 16		- Signed			-32,768 .. 32,767
unsigned int 				= uint32_t - 32	 	- Unsigned		0 .. 4,294,967,295
int									= int32_t  - 32		- Signed			-2,147,483,648 .. 2,147,483,647
unsigned long long 	=	uint64_t - 64		- Unsigned		0 .. 18,446,744,073,709,551,615
long long 					= int64_t	 - 64		- Signed			-9,223,372,036,854,775,808 .. 9,223,372,036,854,775,807
*/
#include <stdint.h>
#include <stdlib.h>

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
#define FLASH_MEM ((1024 * sizeof(char))*(256-8)) // 8k is used for bootloader
#define SRAM ((1024 * sizeof(char)) * 8)
#define EEPROM ((1024 * sizeof(char)) * 4)

/*
* Memory which can be used
*/
#define FREE_SRAM (SRAM - 1024)


/*
Defined structure for linked list, where are all blocks stored
*/
typedef struct MEM_BLOCK
{
	struct MEM_BLOCK *pNextFreeBlock; // pointer to next free block in list of free blocks
	struct MEM_BLOCK *pPrevBlock;  // previous physical memory block
	uint16_t blockSize; // size of actual block
} Mem_block;


/*
* Size of memory block used by this allocator
*/
#define MEM_BLOCK_SIZE sizeof(Mem_block)

/*
* Prepares data structure Linked list, where blocks are stored
* Must be called before using bMemAlloc function.
* @params 
*/
void bMemInit();


/*
* Allocates memory block and returns pointer to memory space
* 
* @param requestedSize Amount of memory to be allocated and accessible from returned pointer
*/
void *bMemAlloc(unsigned int requestedSize);


/*
* Pointer that was used will be set free and inserted to the right place in the linked list
* of free memory blocks, so list stays sorted
* 
@param ptrToFree Pointer to memory which will be set free
*/
void bMemFree(void *ptrToFree);


/*
* Pointer has assigned some amount of memory. Use this function to change memory space
* assigned to pointer. Memory space can be either increased or decreased
*
* @param ptrToRealloc The pointer to memory space which will be reallocated
*
* @param requestedSize New amount of memory which will be assigned to ptrToRealloc
*/
void *bMemRealloc(void *ptrToRealoc, uint16_t requestedSize);

/*
 Prints actual whole linked list of memory blocks
*/
void bPrintLinkedList();


/*
* Print whole memory blocks
*/
void bPrintWholeMemory();

/*
* Print whole physical memory reverse
* This print is based on iterating through pointers which point to previous memory block
* Starts at the End and iterates to the Start
*/
void bPrintWholeMemoryReverse();

#endif
