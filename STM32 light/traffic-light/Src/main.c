/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2020 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "tim.h"
#include "usart.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
#define RXBUFFERSIZE  256     //最大接收字节数

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
void SEG_ZERO(void);
void SEG_ONE(void);
void SEG_TWE(void);
void SEG_THREE(void);
void SEG_FORT(void);
void SEG_FIRE(void);
void SEG_SIXC(void);
void SEG_SEVEN(void);
void SEG_EIGHT(void);
void SEG_NINE(void);
void SEG_OFF(void);
void Display(uint8_t xbit,uint8_t num);
void Traffic_Dis(uint8_t collow);  //0-red,1-yellow,2-greed
void Traffic_Dis_off(void);

uint8_t rxtext[5];
uint8_t txtext[5];
uint8_t aRxBuffer;					//接收中断缓冲
uint8_t Uart1_Rx_Cnt = 0;		//接收缓冲计数
char RxBuffer[RXBUFFERSIZE];   //接收数据
uint8_t tchi;
uint16_t tnum;
uint8_t txbuff[] = "off";
/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */
  

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_TIM2_Init();
  MX_USART1_UART_Init();
  /* USER CODE BEGIN 2 */
	HAL_TIM_Base_Start_IT(&htim2); //启动定时器2中断
	HAL_UART_Receive_IT(&huart1,(uint8_t *)&aRxBuffer,1);			// Enable the USART1 Interrupt
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
	tnum=0;
	Traffic_Dis_off();
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
		Traffic_Dis(tchi);
		Display(0,tnum%10);
		Display(1,tnum/10);
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Initializes the CPU, AHB and APB busses clocks 
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.HSEPredivValue = RCC_HSE_PREDIV_DIV1;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL9;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /** Initializes the CPU, AHB and APB busses clocks 
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
	if (htim->Instance == htim2.Instance)
		{
			static uint8_t b=0;
			static uint16_t a=0;
			a++;
			if(a==1000-1)
			{
				if(tnum!=0) 
				{
					tnum=tnum-1;
					HAL_UART_Transmit_IT(&huart1,(uint8_t*)tnum,10);
				}
				if(tnum == 1) 
				{
					HAL_UART_Transmit_IT(&huart1,(uint8_t*)txbuff,10);
				}
				if(b==0)
				{
					HAL_GPIO_WritePin(GPIOB,LED_Pin,GPIO_PIN_RESET);
				}
				else
				{
					HAL_GPIO_WritePin(GPIOB,LED_Pin,GPIO_PIN_SET);
				}
				b=!b;
				a=0;
			}
		}
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
	if (huart->Instance == huart1.Instance)
	{
		if(Uart1_Rx_Cnt >= 255)  //溢出判断
		{
			Uart1_Rx_Cnt = 0;
			memset(RxBuffer,0x00,sizeof(RxBuffer)); //清空数组
			HAL_UART_Transmit(&huart1, (uint8_t *)"数据溢出", 10,0xFFFF); 				
		}
		else
		{
			RxBuffer[Uart1_Rx_Cnt++] = aRxBuffer;   //接收数据转存
			if((RxBuffer[Uart1_Rx_Cnt-1] == 0x0A)&&(RxBuffer[Uart1_Rx_Cnt-2] == 0x0D)) //判断结束位
			{
				tnum=(atoi(RxBuffer))%10;
				//tnum=(RxBuffer[1]*10)+RxBuffer[2];
				tchi=RxBuffer[2];
//				int i,j;
//				j=0;
//				for(i=0;RxBuffer[i]!='\0';i++)
//				{
//					if(RxBuffer[i]>='0' && RxBuffer[i]<='9')
//					{
//						txtext[j]=txtext[i]-'0';
//						j++;
//					}
//				}
//				HAL_UART_Transmit(&huart1, (uint8_t *)&RxBuffer, Uart1_Rx_Cnt,0xFFFF); //将收到的信息发送出去
//				while(HAL_UART_GetState(&huart1) == HAL_UART_STATE_BUSY_TX)//检测UART发送结束
			
				Uart1_Rx_Cnt = 0;
				memset(RxBuffer,0x00,sizeof(RxBuffer)); //清空数组
			}
		}
		HAL_UART_Receive_IT(&huart1, (uint8_t *)&aRxBuffer, 1);   //再开启接收中断
	}
}


void SEG_ZERO() //0
{
	HAL_GPIO_WritePin(GPIOB,SEG_A_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_B_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_C_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_D_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_E_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_F_Pin,GPIO_PIN_RESET);
}

void SEG_ONE()  //1
{
	HAL_GPIO_WritePin(GPIOB,SEG_B_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_C_Pin,GPIO_PIN_RESET);
}
void SEG_TWE()  //2
{
	HAL_GPIO_WritePin(GPIOB,SEG_A_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_B_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_G_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_E_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_D_Pin,GPIO_PIN_RESET);
}
	
void SEG_THREE()  //3
{
	HAL_GPIO_WritePin(GPIOB,SEG_A_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_B_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_C_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_D_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_G_Pin,GPIO_PIN_RESET);
}
	
void SEG_FORT()  //4
{
	HAL_GPIO_WritePin(GPIOB,SEG_B_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_C_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_G_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_F_Pin,GPIO_PIN_RESET);
}

void SEG_FIRE()  //5
{
	HAL_GPIO_WritePin(GPIOB,SEG_A_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_F_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_G_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_C_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_D_Pin,GPIO_PIN_RESET);
}

void SEG_SIXC()  //6
{
	HAL_GPIO_WritePin(GPIOB,SEG_A_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_F_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_C_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_D_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_E_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_G_Pin,GPIO_PIN_RESET);
}
	
void SEG_SEVEN()  //7
{
	HAL_GPIO_WritePin(GPIOB,SEG_A_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_B_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_C_Pin,GPIO_PIN_RESET);
}

void SEG_EIGHT()  //8
{
	HAL_GPIO_WritePin(GPIOB,SEG_A_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_B_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_C_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_D_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_E_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_F_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_G_Pin,GPIO_PIN_RESET);
}

void SEG_NINE()  //9
{
	HAL_GPIO_WritePin(GPIOB,SEG_A_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_B_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_C_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_D_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_F_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOB,SEG_G_Pin,GPIO_PIN_RESET);
}

void SEG_OFF()  //OFF
{
	HAL_GPIO_WritePin(GPIOB,SEG_A_Pin,GPIO_PIN_SET);
	HAL_GPIO_WritePin(GPIOB,SEG_B_Pin,GPIO_PIN_SET);
	HAL_GPIO_WritePin(GPIOB,SEG_C_Pin,GPIO_PIN_SET);
	HAL_GPIO_WritePin(GPIOB,SEG_D_Pin,GPIO_PIN_SET);
	HAL_GPIO_WritePin(GPIOB,SEG_E_Pin,GPIO_PIN_SET);
	HAL_GPIO_WritePin(GPIOB,SEG_F_Pin,GPIO_PIN_SET);
	HAL_GPIO_WritePin(GPIOB,SEG_G_Pin,GPIO_PIN_SET);
}

void Display(uint8_t xbit,uint8_t num)
{
	HAL_GPIO_WritePin(GPIOB,BIT0_Pin,GPIO_PIN_SET);
	HAL_GPIO_WritePin(GPIOB,BIT1_Pin,GPIO_PIN_SET);
	if(xbit == 0) HAL_GPIO_WritePin(GPIOA,BIT0_Pin,GPIO_PIN_RESET);
	else if(xbit == 1) HAL_GPIO_WritePin(GPIOA,BIT1_Pin,GPIO_PIN_RESET);
	switch(num)
	{
		case 0:
			SEG_ZERO();
      break;
		case 1:
			SEG_ONE();
      break;
		case 2:
			SEG_TWE();
      break;
		case 3:
			SEG_THREE();
      break;
		case 4:
			SEG_FORT();
      break;
		case 5:
			SEG_FIRE();
      break;
		case 6:
			SEG_SIXC();
      break;
		case 7:
			SEG_SEVEN();
      break;
		case 8:
			SEG_EIGHT();
      break;
		case 9:
			SEG_NINE();
      break;
	}
	HAL_Delay(2);
	SEG_OFF();
}

void Traffic_Dis(uint8_t collow)  //0-red,1-yellow,2-greed
{
	if(collow == 0) HAL_GPIO_WritePin(GPIOC,RED_Pin,GPIO_PIN_RESET);
	else if(collow == 1) HAL_GPIO_WritePin(GPIOC,YELLOW_Pin,GPIO_PIN_RESET);
	else if(collow == 2) HAL_GPIO_WritePin(GPIOC,GREED_Pin,GPIO_PIN_RESET);
}

void Traffic_Dis_off()
{
	HAL_GPIO_WritePin(GPIOC,RED_Pin,GPIO_PIN_SET);
	HAL_GPIO_WritePin(GPIOC,YELLOW_Pin,GPIO_PIN_SET);
	HAL_GPIO_WritePin(GPIOC,GREED_Pin,GPIO_PIN_SET);
}

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */

  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{ 
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     tex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
