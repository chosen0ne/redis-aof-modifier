Redis-AOF-Modifier
===============================

本系列脚本用于redis aof的过滤和恢复。  

###1. 主要包括：  
####1) aof_filter.py  
用于过滤aof中的指定命令，适用于恢复大量数据。  
输出3个文件:  
- appendonly.aof.filtered: 输出被过滤掉的命令，即匹配COMMAND,KEY的命令  
- appendonly.aof.filtered_readable: appendonly.aof.filtered的可读模式  
- appendonly.aof.new: 过滤掉相关命令的aof文件，之后需要通过这个文件作为aof恢复redis  
.e.g  
> python aof_filter.py -i appendonly.aof -p 'del,a-delete-key'

####2) aof_fetch.py  
  用于从aof中捞回指定key的数据，适用于恢复少量数据。  
  输出4个文件:  
- appendonly.aof.fetch: 输出所有匹配该KEY的命令  
- appendonly.aof.fetch_readable: appendonly.aof.fetch的可读格式  
- appendonly.aof.filtered: 输出要找回的命令，即匹配COMMAND,KEY的命令  
- appendonly.aof.filtered_readable: appendonly.aof.filtered的可读格式  
.e.g  
> python aof_fetch.py -i appendonly.aof -p 'set,a-delete-key'

####3) aof_redo.py  
   用于redo aof中的命令，通常用于aof_fetch.py输出的结果，以便恢复对应的数据  
.e.g  
> python aof_redo.py -i appendonly.aof.filtered -H 127.0.0.1 -p 6379
   
###2. 命令格式  
通过正则表达式描述需要过滤的命令，格式：

        COMMAND,KEY[,SUB-KEY]       # SUB-KEY可选  
    
对于一层结构，比如string，可以只指定COMMAND,KEY。对于两层结构，恢复该key内容时，可以指定SUB-KEY。  
COMMAND大小写不敏感，KEY和SUB-KEY大小写敏感。  
e.g.  
> del,test-a  => 过滤del test-a  
> hdel,test-b,sub-c   => 过滤hdel test-b sub-c  

对于批量删除操作，比如命令del a b c，指定的命令匹配模式为del b，会保留del a c，删除掉del b。  

###3. NOTICE  
1) 运行结果会包括过滤命令的可读格式，恢复时先通过这个文件确定过滤是否符合预期。  
2) aof-redo.py需要依赖redis-py。  
3) 各个脚本支持-h，可以查看具体的配置选项。  
4) 如果aof文件比较大，过滤和redis加载都需要时间，即需要对aof进行两次扫描。所以尽量使用aof_fetch.py，在其不适用的情况下，再使用aof_filter.py。
