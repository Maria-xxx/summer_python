class people:
    #类属性，属于类本身，所有对象共享
    name = ''
    age = 0
    #私有属性：双下划线 __ 开头，类外部不能直接访问
    __weight = 0

    #构造方法：创建对象的时候自动执行，初始化实例属性
    def __init__(self,n,a,w):
        self.name = n      #self代表实例对象本身，给对象赋值名字
        self.age = a       #年龄
        self.__weight = w  #体重，私有属性

    def speak(self):
        print("%s 说: 我 %d 岁。" %(self.name,self.age))

class student(people): #括号里写父类名字，实现单继承
      grade = '' #新增类属性：年级
      def __init__(self,n,a,w,g):
        #手动调用父类的构造函数，把名字、年龄、体重交给父类初始化
        people.__init__(self,n,a,w)
        self.grade = g #子类新增实例属性：年级
    #重写(覆写)父类的speak方法
      def speak(self):
        print("%s 说: 我 %d 岁了，我在读 %d 年级"%(self.name,self.age,self.grade))


s = student('ken',10,60,3)
# 参数依次传给 __init__：n='ken'名字，a=10年龄，w=60体重，g=3年级
s.speak()