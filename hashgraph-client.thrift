namespace py thrift_gen

struct Status {
  1: string status,
  2: optional i32 consensus_time,
}

service Transaction {
   string transfer(1:i32 payload, 2:i32 target)

   Status status(1:string tx_id)
}