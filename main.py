import sublime, sublime_plugin   # 插件主程序必须要引用这两个基础类库。
import re   # 本插件需要用到的正则表达式类库。
class PasteWithoutBlankLinesCommand(sublime_plugin.TextCommand): 
    """
       进行多行注释：每个菜单命令都对应于一个类。注意类名的写法，是把菜单命令的下划线去掉，改成驼峰式写法，并且在末尾加上Command。
        括号中 sublime_plugin.TextCommand 是此类的父类，表示此类是一个命令菜单的实际行为类。
        如果不是命令菜单引起的而是由于窗口命令引起的实际行为类，父类就要指定为 sublime_plugin.WindowCommand 。
    """
    def run(self, edit):  # def表示定义一个方法。ST插件机制会自动调用指令类的run方法，所以必须重载实现此方法以供执行。
        s = sublime.get_clipboard()     # 获取剪切板内容
        """
       从ST文件视图配置中读取默认行结束符的类别（用操作系统环境表示）。因为不同的操作系统对硬回车的表示和存储方式不同，而这个插件正是需要对这些进行处理。如果你的插件也涉及操作系统的分别或者是配置的分别，都需要考虑按此方法先读取相应的配置，再根据配置进行不同的处理。
        """
        line_ending = self.view.settings().get('default_line_ending') 
        # 根据不同的操作系统环境进行不同的替换处理。
        if line_ending == 'windows': 
            s = re.compile('\n\r').sub('',s) 
            s = re.compile('\r\n\s*\r\n').sub('\r\n',s) 
        elif line_ending == 'mac': 
            s = re.compile('\r\r').sub('\r',s) 
            s = re.compile('\r\s*\r').sub('\r',s) 
        else: # unix / system
            s = re.compile('\n\n').sub('\n',s) 
            s = re.compile('\n\s*\n').sub('\n',s) 
        sublime.set_clipboard(s)    # 修改剪贴板内容，此方法可使减肥过的剪贴板内容在别处也能使用
        self.view.run_command('paste')    # 调用粘贴命令
