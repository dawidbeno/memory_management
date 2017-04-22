// src - Version: Latest
#include <Arduino_FreeRTOS.h>
#include <croutine.h>
#include <event_groups.h>
#include <FreeRTOSConfig.h>
#include <FreeRTOSVariant.h>
#include <list.h>
#include <mpu_wrappers.h>
#include <portable.h>
#include <portmacro.h>
#include <projdefs.h>
#include <queue.h>
#include <semphr.h>
#include <StackMacros.h>
#include <task.h>
#include <timers.h>
#include <avr/eeprom.h>
#include <Arduino.h>
#include <stdlib.h>

#include <bestFit_MemManag_EEPROM.h>

void TaskMain( void *pvParameters );
void TaskTestBlink( void *pvParameters );

/* Algorithm constants */
#define BEST 'b'
#define WORST 'w'
#define NUM_POINTERS 500   //max num of blocks is 509 (2078 / 8)

/* Actual algorithm
* Default algorithm is BEST fit
*/
char actAlg = BEST;

uint16_t ptrArray[NUM_POINTERS]; // array where pointers are stored

int isInitialized = 0;


// the setup function runs once when you press reset or power the board
void setup() {


  Serial.begin(9600);
  while( !Serial ){
    ;
  }


  xTaskCreate(
    TaskMain
    ,  (const portCHAR *) "Main function"
    ,  1000 // This stack size can be checked & adjusted by reading Highwater
    ,  NULL
    ,  1  // priority
    ,  NULL );

    xTaskCreate(
      TaskTestBlink
      ,  (const portCHAR *) "testovanie2"
      ,  128 // This stack size can be checked & adjusted by reading Highwater
      ,  NULL
      ,  2  // priority
      ,  NULL );

  // Now the task scheduler, which takes over control of scheduling individual tasks, is automatically started.
}

void loop()
{
  // Empty. Things are done in Tasks.
}
/*--------------------------------------------------*/
/*---------------------- Functions ---------------------*/
/*--------------------------------------------------*/


void clearPtrArr(){
  for(int i=0; i<NUM_POINTERS; i++){
    ptrArray[i] = 0;
  }
}


/* Must be called before any allocation
  Memory is isInitialized
  Array with pointers to all allocated memory blocks is allocated and initialized
 */
void initComm(){
  if(actAlg == BEST){
   bMemInit();
   clearPtrArr();
    isInitialized = 1;
  }else{
    //wMemInit();
    clearPtrArr();
    isInitialized = 1;
  }

  if(isInitialized == 1){
    Serial.println("INIT");
  }

}

/*Change algorithm*/
void setAlg(char alg){
  actAlg = alg;
  if(actAlg == BEST){
    bMemInit();
    clearPtrArr();
    isInitialized = 1;
  }else{
    //wMemInit();
    clearPtrArr();
    isInitialized = 1;
  }
  if(isInitialized == 1){
    Serial.print("Alg changed to:");Serial.println(actAlg);
  }
}






/* Provides test allocation*/
void allocate(int size){
  uint16_t ptr;
  int i;
  if(actAlg == BEST){
    ptr = bMemAlloc((uint16_t)size);
    while(ptrArray[i] != 0){
      i++;
    }
    ptrArray[i] = ptr;

  }else if(actAlg == WORST){
    //arr = (char*)wMemAlloc(size);
  }

  if(ptrArray[0] != NONE){
    Serial.print("Allocation SUCCESS:");Serial.println(i);
  }else{
    Serial.println("Allocation FAILED");
  }

}


void freeMem(int ptr){
    Serial.print("Free address:");Serial.println(ptrArray[ptr]);
    Serial.print("ptrArray: ");Serial.println(ptr);
    bMemFree(ptrArray[ptr]);
    ptrArray[ptr] = 0;
}



void reallocMem(int ptr, int size){
    uint16_t ptrToRealloc = ptrArray[ptr];
    uint16_t newPtr = bMemRealloc(ptrToRealloc, (uint16_t)size);
    ptrArray[ptr] = newPtr;
}






/*--------------------------------------------------*/
/*---------------------- Tasks ---------------------*/
/*--------------------------------------------------*/


void TaskMain(void *pvParameters)  // This is a task.
{
  (void) pvParameters;
  int counter = 0;



  /* Main loop */
  for(;;){

    if(counter < 4){
      Serial.print("Counter: ");Serial.println(counter);
      counter++;
    }

    if(Serial.available() > 0){
      /*Read input byte*/
      char inChar = (char)Serial.read();


      /* Initialize communication between PC and Arduino*/
      if(inChar == 'i'){
        initComm();
        counter = 0;
        continue;
      }

      /*Set algorithm to BEST fit*/
      if(inChar == 'b'){
        setAlg(BEST);
        counter = 0;
        continue;
      }

      /*Set algorithm to WORST fit*/
      if(inChar == 'w'){
        setAlg(WORST);
        counter = 0;
        continue;
      }

      /* Allocates */
      if(inChar == 'a'){
        char pocChar = (char)Serial.read(); //number of digits in number
        int poc = pocChar - '0';
        char numStr[poc];
        int i, size;

        /* Create number from incomming bytes */
        for(i=0; i<poc; i++){
          numStr[i] = (char)Serial.read();
        }

        size = atoi(numStr);
        Serial.print("Size: ");Serial.println(size);
        allocate(size);

        counter = 0;
        continue;
      }

      /*Free memory*/
      if(inChar == 'f'){
        char pocChar = (char)Serial.read(); //number of digits in number
        int poc = pocChar - '0';
        char numStr[poc];
        int i, addr;

        /* Create number from incomming bytes */
        for(i=0; i<poc; i++){
          numStr[i] = (char)Serial.read();
        }

        addr = atoi(numStr);
        freeMem(addr);
        Serial.println("Free complete");
        counter = 0;
        continue;
      }

      /*Realloc block*/
      if(inChar == 'r'){
        // get pointer
        char pocChar = (char)Serial.read(); //number of digits in number
        int poc = pocChar - '0';
        char numStr[poc];
        int i, ptr;
        for(i=0; i<poc; i++){
          numStr[i] = (char)Serial.read();
        }
        ptr = atoi(numStr);

        // get size
        char pocChar2 = (char)Serial.read(); //number of digits in number
        int poc2 = pocChar2 - '0';
        char numStr2[poc];
        int j, sizeToRealloc;
        for(j=0; j<poc2; j++){
          numStr2[j] = (char)Serial.read();
        }
        sizeToRealloc = atoi(numStr2);

        Serial.print("ptr: ");Serial.println(ptr);
        Serial.print("size: ");Serial.println(sizeToRealloc);

        reallocMem(ptr, sizeToRealloc);
        Serial.println("Realloc complete");

        continue;
      }


      /*Prints list of free blocks. Memory must be initialized*/
      if(inChar == 'p' && isInitialized == 1){
        if(actAlg == BEST){
        //  bPrintLinkedList();
          bPrintWholeMemory();
          Serial.println("Finish");
          continue;
        }
        if(actAlg == WORST){
          //wPrintLinkedList();
          //wPrintLinkedList();
          Serial.println("Finish");
          counter = 0;
        }
      }else if(isInitialized == 0){
        Serial.println("Memory was not initialized");
      }

    }

    vTaskDelay( 100 / portTICK_PERIOD_MS );
  }

}


void TaskTestBlink(void *pvParameters)  // This is a task.
{
  (void) pvParameters;
 pinMode(13, OUTPUT);
for(;;){
  //Serial.print("init");Serial.println(actAlg);
        digitalWrite(13, HIGH);   // turn the LED on (HIGH is the voltage level)
        vTaskDelay( 1000 / portTICK_PERIOD_MS ); // wait for one second
        digitalWrite(13, LOW);    // turn the LED off by making the voltage LOW
        vTaskDelay( 1000 / portTICK_PERIOD_MS );
}

}
