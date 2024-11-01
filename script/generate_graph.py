import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 创建 DataFrame 来存储表格中的数据
data = {
    "Device": ["NVIDIA A100", "ASCEND 910B", "ASCEND 910B-Mindie"],
    "Sucessful Req.": [500, 500, 500],  # 如果你有具体数据，可以在这里填充
    "Tput (req/s)": [3.74, 3.04, 3.51],
    "Mean TTFT (ms)": [20.58, 69.24, 35.4],
    "Std TTFT (ms)": [18.95, 67.26, 39.20],
    "Mean ITL (ms)": [16.2997, 73.99, 40.20],
    "Std ITL (ms)": [8.53774, 46.76, 40.61],
    "Input Tput (tok/s)": [755.813, 613.95, 709.27],
    "Output Tput (tok/s)": [499.251, 397.56, 454.02]
}

# 转换为 Pandas DataFrame
df = pd.DataFrame(data)

# 转换为 Pandas DataFrame
df = pd.DataFrame(data)

# 设置图表的大小和子图的布局
fig, axs = plt.subplots(2, 3, figsize=(14, 8))  # 两行三列的子图布局
fig.suptitle('Performance Metrics for Different Devices', fontsize=16)

# 配置图表颜色
colors = ['skyblue', 'orange', 'green']

# 绘制不同的子图
# 第一行，绘制吞吐量（Tput）、平均 TTFT 和 TTFT 标准差
axs[0, 0].bar(df['Device'], df['Tput (req/s)'], color=colors)
axs[0, 0].set_title('Tput (req/s)')
axs[0, 0].set_ylabel('Tput (req/s)')
axs[0, 0].tick_params(axis='x', rotation=0)

axs[0, 1].bar(df['Device'], df['Mean TTFT (ms)'], color=colors)
axs[0, 1].set_title('Mean TTFT (ms)')
axs[0, 1].set_ylabel('Mean TTFT (ms)')
axs[0, 1].tick_params(axis='x', rotation=0)

axs[0, 2].bar(df['Device'], df['Std TTFT (ms)'], color=colors)
axs[0, 2].set_title('Std TTFT (ms)')
axs[0, 2].set_ylabel('Std TTFT (ms)')
axs[0, 2].tick_params(axis='x', rotation=0)

# 第二行，绘制 Mean ITL、Std ITL、输入和输出吞吐量
axs[1, 0].bar(df['Device'], df['Mean ITL (ms)'], color=colors)
axs[1, 0].set_title('Mean ITL (ms)')
axs[1, 0].set_ylabel('Mean ITL (ms)')
axs[1, 0].tick_params(axis='x', rotation=0)

axs[1, 1].bar(df['Device'], df['Std ITL (ms)'], color=colors)
axs[1, 1].set_title('Std ITL (ms)')
axs[1, 1].set_ylabel('Std ITL (ms)')
axs[1, 1].tick_params(axis='x', rotation=0)

# 输入与输出吞吐量合并为一张图
axs[1, 2].bar(df['Device'], df['Input Tput (tok/s)'], width=0.3, label='Input Tput', align='center', color='lightcoral')
axs[1, 2].bar(df['Device'], df['Output Tput (tok/s)'], width=0.3, label='Output Tput', align='edge', color='lightseagreen')
axs[1, 2].set_title('Input & Output Tput (tok/s)')
axs[1, 2].set_ylabel('Token/s')
axs[1, 2].legend()
axs[1, 2].tick_params(axis='x', rotation=0)

# 布局调整，避免重叠
plt.tight_layout(rect=[0, 0, 1, 0.95])

# 显示图表
plt.show()