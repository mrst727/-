# 篮球外线隐藏评分 Skill

把整个 `basketball-outside-hidden` 文件夹放进支持 Skills 的 Codex 本地技能目录。
通常使用 `~/.agents/skills/`，Windows 对应 `%USERPROFILE%\.agents\skills\`；如客户端指定了其他目录，以该目录为准。
最终结构应是 `skills/basketball-outside-hidden/SKILL.md`，不要重复嵌套两层同名目录。
重新打开会话，使客户端重新发现技能。

安装后发送球员的外线进攻模拟截图，并说：

> 用 basketball-outside-hidden 分析这张图，给我外攻隐藏评分、范围和高低判断。

也可直接发文本：

> 外攻30.52/57.35，两分82，三分71，突破65，无球83，无后仰和急停加成。

有徽章时补充真实等级和加成，例如“后仰+23，无其他相关加成”。不清楚也可以分析，会先给含加成结果。

本Skill不需要联网、REA、Node.js或完整APK；计算脚本需要Python 3。支持执行脚本的智能体会自动调用，没有运行环境时可按Skill内公式手算并标注。
在已经下载文件的当前云工作区，也可以直接要求智能体读取此目录的SKILL.md后分析，无需声称它已自动注册到当前会话。

示例结果见 `references/method.md`；模板参考阈值来自上传版本，非硬上限。
