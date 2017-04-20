#include <avr/eeprom.h>
#include <Arduino.h>

typedef struct MEM_BLOCK
{
  int pNextFreeBlock; // pointer to next free block in list of free blocks
  int pPrevBlock;  // previous physical memory block
  int blockSize; // size of actual block
} Mem_block;

Mem_block Start;
Mem_block End;
Mem_block Act;
int pActBlock = 0;

void setup()
{
  Serial.begin(9600);
  while(!Serial){
    ;
  }

  Start.pNextFreeBlock = 200;
  Start.pPrevBlock = 0;
  Start.blockSize = 0;

  //eeprom_write_block(&Start, (uint16_t*)pActBlock, sizeof(Mem_block));

  Act.pNextFreeBlock = 400;
  Act.pPrevBlock = 0;
  Act.blockSize = 4070;

  pActBlock = Start.pNextFreeBlock;
  //eeprom_write_block(&Act, (uint16_t*)pActBlock, sizeof(Mem_block));

  End.pNextFreeBlock = 5000;
  End.pPrevBlock = 200;
  End.blockSize = 4096;

  pActBlock = Act.pNextFreeBlock;
  //eeprom_write_block(&End, (uint16_t*)pActBlock, sizeof(Mem_block));

  Serial.println("Data retreived");
  //
  // pActBlock = 0;
  // eeprom_read_block(&Act, (uint16_t*)pActBlock, sizeof(Mem_block));
  // Serial.println(Act.blockSize);
  //
  // pActBlock = Act.pNextFreeBlock;
  // eeprom_read_block(&Act, (uint16_t*)pActBlock, sizeof(Mem_block));
  // Serial.println(Act.blockSize);
  //
  // pActBlock = Act.pNextFreeBlock;
  // eeprom_read_block(&Act, (uint16_t*)pActBlock, sizeof(Mem_block));
  // Serial.println(Act.blockSize);

  pActBlock = 0;
  while(1){
    eeprom_read_block(&Act, (uint16_t*)pActBlock, sizeof(Mem_block));
    Serial.println(Act.blockSize);
    if(Act.pNextFreeBlock > 4096){
      break;
    }
    pActBlock = Act.pNextFreeBlock;
  }



}

void loop()
{
}
