<?php

class father {

    public function __construct(){
        echo "父类构造函数，如果子类没有重写构造函数将会调用这里。如果子类重写了构造函数则子类不用自动调用这个函数，而需要显示调用父类构造函数。";
    }

    public $m_fa="fa";
    protected $m_fb="fb";
    private $m_fc="fc";

    public function getFa(){return $m_fa;}
    protected function getFb(){return $m_fb;}
    private function getFc(){return $m_fc;}
    public function getFaPrivate_1(){return $m_fc;}
    public function getFaPrivate_2(){return $m_fc;}

    public function getAll(){
        echo $this->m_fa, $this->m_fb, $this->m_fc;
        echo  $this->getFa(), $this->getFb(), $this->getFc();
    }

}

class son extends father{
    public function __construct(){
        parent::__construct(); //显示调用父类构造函数。
        echo "子类构造函数调用";
    }
}

$class_fa = 'father';
$class_son = 'son';
$fa = new $class_fa();
$fa->getAll();
$son = new $class_son();
$son->getFa();
// 执行以下方法回报错，protected 无法在类外面进行调用的
// 报错信息：Fatal error: Uncaught Error: Call to protected method father::getFb()...
// $son->getFb();
// 执行以下方法回报错，private 无法被继承，也无法在类外面进行调用的
// 报错信息：Fatal error: Uncaught Error: Call to private method father::getFc()...
// $son->getFc();

$son->getFaPrivate_2();
?><?php
/**
 * Define MyClass
 */
class MyClass
{
    public $public = 'Public';
    protected $protected = 'Protected';
    private $private = 'Private';

    function printHello()
    {
        echo $this->public;
        echo $this->protected;
        echo $this->private;
    }
}

$obj = new MyClass();
echo $obj->public; // 这行能被正常执行
echo $obj->protected; // 这行会产生一个致命错误
echo $obj->private; // 这行也会产生一个致命错误
$obj->printHello(); // 输出 Public、Protected 和 Private


/**
 * Define MyClass2
 */
class MyClass2 extends MyClass
{
    // 可以对 public 和 protected 进行重定义，但 private 而不能
    protected $protected = 'Protected2';

    function printHello()
    {
        echo $this->public;
        echo $this->protected;
        echo $this->private;
    }
}

$obj2 = new MyClass2();
echo $obj2->public; // 这行能被正常执行
echo $obj2->private; // 未定义 private
echo $obj2->protected; // 这行会产生一个致命错误
$obj2->printHello(); // 输出 Public、Protected2 和 Undefined

?>
<?php
/**
 * Define MyClass
 */
class MyClass
{
    // 声明一个公有的构造函数
    public function __construct() { }

    // 声明一个公有的方法
    public function MyPublic() { }

    // 声明一个受保护的方法
    protected function MyProtected() { }

    // 声明一个私有的方法
    private function MyPrivate() { }

    // 此方法为公有
    function Foo()
    {
        $this->MyPublic();
        $this->MyProtected();
        $this->MyPrivate();
    }
}

$myclass = new MyClass;
$myclass->MyPublic(); // 这行能被正常执行
$myclass->MyProtected(); // 这行会产生一个致命错误
$myclass->MyPrivate(); // 这行会产生一个致命错误
$myclass->Foo(); // 公有，受保护，私有都可以执行


/**
 * Define MyClass2
 */
class MyClass2 extends MyClass
{
    // 此方法为公有
    function Foo2()
    {
        $this->MyPublic();
        $this->MyProtected();
        $this->MyPrivate(); // 这行会产生一个致命错误
    }
}

$myclass2 = new MyClass2;
$myclass2->MyPublic(); // 这行能被正常执行
$myclass2->Foo2(); // 公有的和受保护的都可执行，但私有的不行

class Bar 
{
    public function test() {
        $this->testPrivate();
        $this->testPublic();
    }

    public function testPublic() {
        echo "Bar::testPublic\n";
    }
    
    private function testPrivate() {
        echo "Bar::testPrivate\n";
    }
}

class Foo extends Bar 
{
    public function testPublic() {
        echo "Foo::testPublic\n";
    }
    
    private function testPrivate() {
        echo "Foo::testPrivate\n";
    }
}

$myFoo = new foo();
$myFoo->test(); // Bar::testPrivate 
                // Foo::testPublic
?>
