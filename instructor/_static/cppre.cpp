#include <string>
#include <iostream>

class Parent {
private:
  std::string _name;

public:
  Parent(const std::string& name){
	  _name = name;
  }
  virtual ~Parent(){
	  std::cout << "Parent dtor" << std::endl; 
  }
  virtual void print(){
	  std::cout << "I am named " << _name << std::endl;
  }
};

class Child : public Parent {
private:
  int _value;
  
public:
  Child(const std::string& name, const int value) : Parent(name) {
	  _value = value;
  }
  virtual ~Child(){ std::cout << "Child dtor" << std::endl; }
  virtual void print(){
	  Parent::print();
	  std::cout << "I have value " << _value << std::endl;
  }
};

int main() {
  
  Parent* p = new Parent("Anakin");
  p->print();

  Child* c = new Child("Luke", 42);
  c->print();
  return 0;
}
