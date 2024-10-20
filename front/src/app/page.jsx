
"use client";

import { useState } from 'react';

export default function Home() {
  const [code, setCode] = useState('');  // 商品コードの状態
  const [itemData, setItemData] = useState(null);  // クエリ結果の状態
  const [message, setMessage] = useState('');
  const [purchaseList, setPurchaseList] = useState([]);  // 購入リストの状態

  const handleCheck = async () =>{
    try{
      const res = await fetch('http://127.0.0.1:8000/check');
      const data = await res.json();
      setMessage(data.message);
    }catch(error){
      console.error('Error fetching data:', error);
    }
  };

  // 商品コード読み込みボタンを押したときの処理
  const handleSubmit = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/items/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code }),  // 商品コードをPOSTする
      });
      const data = await res.json();
      console.log(data);
      setItemData(data);  // 返ってきた商品データを保存
    } catch (error) {
      console.error('Error submitting code:', error);
    }
  };

  // 「追加」ボタンを押したときの処理
  const handleAddToList = () => {
    if (itemData && itemData.prd_id) {  // prd_idがあるか確認
        // 現在の購入リストに新しい商品を追加
          const newItem = {
              prd_id: itemData.prd_id, // 商品ID
              code: code,              // 商品コード
              name: itemData.name,     // 商品名
              price: itemData.price    // 商品価格
            };
      // 現在の購入リストに新しい商品を追加
      setPurchaseList([...purchaseList, newItem]);
       // 商品コードと商品データをリセット（空欄にする）
      setCode('');          // ① 商品コードを空にする
      setItemData(null);     // ② ③ 商品データをリセット
    } else {
    alert("商品情報が正しくありません");
   }
  };


  // 購入ボタンを押したときの処理
  const handlePurchase = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/purchase', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          items: purchaseList,  // 購入リスト
          emp_cd: '9999999999',
          store_cd: '12345',  // 固定のEMP_CD
          pos_no: '30',         // 固定のPOS_NO
          total_amt: '0',       // total_amtは'0'として送信
        }),
      });
      const data = await res.json();
      alert('購入が完了しました');
    } catch (error) {
      console.error('Error processing purchase:', error);
    }
  };


  return (
    <div className="flex flex-col">
    <h1>Hello world</h1>
    <button className="btn btn-neutral w-48" onClick={handleCheck}>check</button>
    {message && <p>受信メッセージ: {message}</p>}

    <p className="text-2xl mt-20">YYY_POSアプリ</p>

    <input
     type="text"
     value={code}
     onChange={(e) => setCode(e.target.value)}  // 入力内容をstateにセット
     placeholder="コードを入力してください"
     className="input input-bordered w-80 max-w-xs mt-4 mb-2" />
    <button className="btn btn-primary w-80 max-w-xs mb-8" onClick={handleSubmit}>商品コード読み込み</button>

{/* データがなくても枠を表示 */}
<div className="flex flex-col">
        <div className="border border-gray-300 p-4 rounded-lg w-80 mb-4">
          <p>{itemData ? itemData.name : '---'}</p>
          </div>
          <div className="border border-gray-300 p-4 rounded-lg w-80 mb-4">
          <p>{itemData ? `${itemData.price}円` : '---'}</p>
          </div>
      </div>

      <button className="btn btn-primary w-80 max-w-xs mb-8"  onClick={handleAddToList}>追加</button>

      <p className="text-2xl mb-2">購入リスト</p>
      <div className="border border-gray-300 p-4 rounded-lg w-1/2 mb-4">
      {purchaseList.length > 0 ? (
      purchaseList.map((item, index) => (
      <div key={index} className="">
        <p>{item.name} ×1 {item.price}円 ＝ {item.price * 1}円</p>
      </div>
          ))
        ) : (
          <p>---</p>
        )}
          </div>

      <button className="btn btn-primary w-80 max-w-xs mb-8" onClick={handlePurchase}>購入</button>
    </div>
  );
}
