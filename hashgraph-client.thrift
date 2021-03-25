namespace py thrift_gen

service Transaction {
   void transfer(1:i32 payload, 2:i32 target)
}