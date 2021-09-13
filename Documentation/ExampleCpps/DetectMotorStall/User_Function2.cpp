
#include "System.h"

uint32_t count = 0;

void Init(UserFunction *pUserFunction){
  
  pUserFunction->m_variable[5] = 0;
  
  return;
  }


uint32_t TuneStallGuard2View(UserFunction *pUserFunction)
{

      TMC5160_Reg::DRV_STATUS_Register drvStatus = { 0 };
      drvStatus = g_Motor1.GetDrvStatus();
      
      return drvStatus.sg_result;
}


uint32_t RunCapture(uint32_t par, UserFunction* pUserFunction)
{
  
  uint32_t last = 0;
  uint32_t last_count = 0;
  uint32_t count = 0;
  uint32_t sum_val = 0;
  bool _run = true;
  pUserFunction->m_variable[5] = 0;
  
  while (_run){
    Serial.print(count);
    Serial.print(" sum val: ");
    Serial.println(sum_val);
      if (count <= 5){
        uint32_t ret = TuneStallGuard2View(pUserFunction);
        sum_val += ret;
        pUserFunction->m_variable[5] = 0;
        

        if (count == 4){
          if (last == ret){
          last_count ++;
          }
        last = ret;
        }
        
        vTaskDelay(100);
      }
      else{
        if (sum_val == 0){
          Serial.println("Stopped moving!");
          pUserFunction->m_variable[5] = 1;
          Serial.print("Variable ! ");
          Serial.println(pUserFunction->m_variable[5]);
          _run = false;
          }
        if (last_count == 5){
          Serial.println("Stopped moving ---> last count!");
          pUserFunction->m_variable[5] = 1;
          Serial.print("Variable ! ");
          Serial.println(pUserFunction->m_variable[5]);
          _run = false;
          
          }    
        sum_val = 0;
        count = 0;
        }
        count ++;
  }

  return 1;
}


uint32_t UserFunction2(uint32_t par, UserFunction* pUserFunction)
{  
  if (par == 0) Init(pUserFunction);
  if (par == 3) RunCapture(par, pUserFunction);
 
  return 1;
}
