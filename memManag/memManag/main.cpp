
#include <stdio.h>
#include "bestFit_MemManag.h"
#include "worstFit_MemManag.h"

void level_1() {
	bMemInit();
	bPrintLinkedList();
	
}

void level_2() {
	printf("LEVEL 2");

}

void level_3() {
	printf("LEVEL 3");

}

void level_4() {
	printf("LEVEL 4");

}



int main() {
	int lvl;

	while (1) {
		printf("\n****************\nZadaj level: \n");
		scanf_s("%d", &lvl);

		switch (lvl) {
		case 1:
			level_1();
			break;
		case 2:
			level_2();
			break;
		case 3:
			level_3();
			break;
		case 4:
			level_4();
			break;
		}
	}


	getchar();
}