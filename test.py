# import threading
#
# def prit1(b):
#     print(1)
#     return 1
#
# def prit2(a):
#     print(2)
#     return 2
#
# threads = []
# t1 = threading.Thread(target=prit1,args=(1,))
# threads.append(t1)
# t2 = threading.Thread(target=prit2,args=(2,))
# threads.append(t2)
#
# for t in threads:
#     # print(3)
#     t.setDaemon(True)
#     t.start()
#
#
arra = ['1','2','3']
print(arra.index('0'))