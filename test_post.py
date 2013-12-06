#-*-coding:utf-8-*-
import QueueClient
import config
import json
import zlib
class WorkTask(QueueClient.Task):
     def StepFinish(self,taskqueueclient):
         print json.dumps(self.result_headers)
         print self.result_body
if __name__ == '__main__':
    work=QueueClient.TaskQueueClient(config.Queue_Server,config.Queue_Port,config.Queue_Path,config.Queue_User,config.Queue_PassWord,'test')
    task=WorkTask()
    task.request_headers={"yes":False}
    task.request_body="shit you"
    work.AddTask(task)
    work.WaitResult()
    work.Close()