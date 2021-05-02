namespace py thrift_gen

struct Status {
  1: string status,
  2: optional i32 consensus_time,
}

service Transaction {
   string transfer(1:i32 payload, 2:i32 target)

   string crypto_transfer(1:binary owner, 2:i32 amount, 3:string receiver, 4:binary challenge, 5:binary signature)

   Status status(1:string tx_id)

   i32 balance(1:string address)
}