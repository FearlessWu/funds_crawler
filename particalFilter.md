## partical filter(粒子滤波)
### 1、mportance sampling(重要性采样)
$$
E(f(x)) = \int_x =f(x)p(x)dx\tag{1}
$$
其中，$x$服从分布$x～p(x)$
进行蒙特卡洛采样：
$$
E(f(x)) \approx \frac{1}{N}\sum_{i=1}^Nf(x^i)\tag{2}
$$
$$
x^{1},x^{2}...x^{N}～p(x)\\
$$
对于高维非高斯非线性的概率分布，我们无法直接获得$p(x)$的概率密度函数，我们希望用能在其他的分布来代替原来的分布采用。假设我们按照我们设定的分布函数$q(x)$对$x$进行采样，不是一般性地，(1)式可以改写成：
$$\begin{aligned}
    E(f(x)) &= \int_x f(x)\frac{p(x)}{q(x)}\cdot q(x) dx
            \approx \frac{1}{N}\sum_{i=1}^Nf(x^i)\frac{p(x^i)}{q(x^i)}\cdot q(x^i)\tag{3}
 
\end{aligned}
$$
其中，$x^{1},x^{2}...x^{N}～q(x)$.<br>
这里的问题是如何选择合适的$q(x)$分布，我们在这里记权$w^i=\frac{p(x^i)}{q(x^i)}$。
### 2、高维度采样
假设:
$$p(x)=\frac{\gamma(x)}{\int f(x)dx}\tag{4}$$
其中$\int f(x)dx$为归一化常数，不会影响样本的相对权重，所以我们只考虑$\gamma$的分布情况。<br>
对于N维的状态，有：
$$
x_{1:N}\equiv{x_1,x_2....x_N}
$$
对应的的权为：
$$
w_{x_{1:N}}^i = \frac{\gamma(x_{1:N}^i)}{q(x_{1:N}^i)}\tag{5}
$$
直接对高维度的状态进行采样对于实际操作来说是十分困难或者说是非常消耗资源的，因为我们可以用边缘概率的思想来递归对高维度状态采样。<br>
对于维度1，可以求 $2:N$ 维的边缘分布有：
$$
\gamma (x_1) = \int_{x_{2:N}}\gamma(x_{1:N})dx_{2:N}\tag{6}
$$
对应的第 $i$ 个样本权重为：
$$
w(x_1^i)=\frac{\gamma(x_1^i)}{q(x_1^i)}\tag{7}
$$
其中 $x_1^i ～ q(x_1)$.<br>
读者需要注意的是本文中上标代表着样本的序号，下表代表的是状态所在的维度。
对于维度2，同理可以得到：
$$
\gamma (x_{1:2}) = \int_{x_{3:N}}\gamma(x_{1:N})dx_{3:N}\tag{6}
$$
对应的第 $i$ 个样本权重为：
$$
w(x_1^i)=\frac{\gamma(x_{1:2}^i)}{q(x_{1:2}^i)}\tag{7}
$$
其中 $x_{1:2}^i ～ q(x_{1:2})$.<br>
对于联合分布的两个状态 $(x_1,x_2)～ p(x_1,x_2)$，如果我们已经对维度1的样本进行采样，根据条件概率有：
$$
x_1^i ～ q(x_1)\\
x_2^i ～ q(x_2|x_1^i)\tag{8}
$$
推广到$N$维，则有：
$$
x_{1:N-1}^i ～ q(x_{1:N-1})\\
x_N^i ～ q(x_N|x_{1:N-1}^i)\tag{8}
$$
因此基于(7)式，我们可以推广到 $1:N$维得：
$$
\begin{aligned}
    w(x_{1:N}^i) &= \frac{\gamma(x_{1:N}^i)}{q(x_{1:N}^i)}\\
    &=\frac{\gamma(x_{1:N}^i)}{q(x_N|x_{1:N-1})\cdot q(x_{1:N-1}^i)}\\
    &=\frac{\gamma(x_{1:N}^i)\cdot \gamma(x_{1:N-1})}{q(x_N|x_{1:N-1})\cdot q(x_{1:N-1}^i)\cdot \gamma(x_{1:N-1})}\\
    &=w(x_{1:N-1}^i)\frac{\gamma(x_{1:N}^i)}{q(x_N|x_{1:N-1})\cdot \gamma(x_{1:N-1})}\tag{9}
\end{aligned}
$$
这样我们得到了 $1:N-1$ 到 $1:N$ 维的递归公式，这样我们可以大大降低高维度的采样难度。
### 3、dynamic model
在时序状态估计中，通常处理不是高维度问题，这里我们可以把上述的高维度问题转化为时间动态问题。对于动态问题，可以获得运动方程和观测方程和相应的条件概率：<br>
<style>
table {
margin: auto;
}
</style>

|||
|:----:|:-----:|
|运动方程|观测方程|
|$x_t=A_t\cdot x_{t-1} + w_t$|$y_t=H_t\cdot x_{t} + \eta_t$|
|$p(x_t\|x_{t-1})$|$p(y_t\|x_{t})$|
|||

上述高维度的$\gamma(x_{1:N})$ 在动态模型中可以表示为 $p(x_{1:t},y_{1:t})$<br>
根据(9)式，动态模型的得权重递推关系为：
$$
\begin{aligned}
    w(x_{1:t}^i) &=w(x_{1:t-1}^i)\frac{p(x^i_{1:t},y^i_{1:t})}{q(x^i_t|x^i_{1:t-1})\cdot p(x^i_{1:t-1},y^i_{1:t-1})}\\
    &=w(x_{1:t-1}^i)\frac{p(y^i_t|x^i_{1:t},y^i_{1:t-1})\cdot p(x^i_{1:t},y^i_{1:t-1})}{q(x^i_t|x^i_{1:t-1})\cdot p(x^i_{1:t-1},y^i_{1:t-1})}\tag{10}

\end{aligned}
$$
因为$y_t$只与$x_t$有关，$x_t$还与$x_{t-1}有关，其他可省略，式(10)可以写为：
$$
\begin{aligned}
    w(x_{1:t}^i)
    &=w(x_{1:t-1}^i)\frac{p(y^i_t|x^i_{1:t})\cdot p(x^i_t|x_{t-1})\cdot p(x^i_{1:t-1},y^i_{1:t-1})}{q(x^i_t|x^i_{1:t-1})\cdot p(x^i_{1:t-1},y^i_{1:t-1})}\\
    &=w(x_{1:t-1}^i)\frac{p(y^i_t|x^i_{1:t})\cdot p(x^i_t|x_{t-1})}{q(x^i_t|x^i_{1:t-1})}\tag{11}
\end{aligned}
$$
其中 $x_t^i～q(x_t^i|x_{t-1}^i)$<br>
这里我们把动态模型的递归公式也讲清楚了。但其实前面的一直没有讲到一个大问题，就是$q$的是一个怎么分布的概率函数，我们的采样原则就是按照我们自己定义的概率分布来采样的。下面我们介绍下$q$的是怎么确定。<br>
根据图模型可知，$x_t$与$y_t$、$x_{t-1}$，所以最佳的$q(x_t）$分布为：
$$
q(x_t) = p(x_t|x_{t-1},y_t)\tag{12}
$$

