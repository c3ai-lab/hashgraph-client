namespace py thrift_gen

struct Status {
  1: string status,
  2: optional i32 consensus_time,
}

// balance transfer data
struct BalanceTransfer {
	1: string senderId;
	2: string receiverId;
	3: i32    amount;
	4: i64	  timestamp;
}

service Transaction {
   string transfer(1:i32 payload, 2:i32 target)

   void crypto_transfer(1:binary owner, 2:i32 amount, 3:string receiver, 4:binary challenge, 5:binary signature)

   Status status(1:string tx_id)

   i32 balance(1:string address)

   binary challenge()
   
   list<BalanceTransfer> balance_history(1:string ownerId)
}