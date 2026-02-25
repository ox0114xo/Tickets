import { useState } from 'react';

export default function Home() {
  const [config, setConfig] = useState({ url: '', zone: '', count: 2 });

  const startGrab = async () => {
    const res = await fetch('/api/start-bot', {
      method: 'POST',
      body: JSON.stringify(config),
    });
    alert("任務已送出！");
  };

  return (
    <div className="p-10 bg-slate-900 min-h-screen text-white">
      <h1 className="text-3xl font-bold mb-6">Kham 搶票控制台</h1>
      <div className="space-y-4">
        <input 
          placeholder="節目網址" 
          className="w-full p-2 text-black"
          onChange={(e) => setConfig({...config, url: e.target.value})}
        />
        <input 
          placeholder="目標區域 (如: 特A區)" 
          className="w-full p-2 text-black"
          onChange={(e) => setConfig({...config, zone: e.target.value})}
        />
        <button 
          onClick={startGrab}
          className="bg-red-600 px-6 py-2 rounded font-bold hover:bg-red-700"
        >
          立即啟動機器人
        </button>
      </div>
    </div>
  );
}

