import { useState } from 'react';
import { LoginScreen } from './components/LoginScreen';
import { ChatScreen } from './components/ChatScreen';

function App() {
  const [username, setUsername] = useState<string>('');

  const handleLogin = (name: string) => {
    setUsername(name);
  };

  const handleLogout = () => {
    setUsername('');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {!username ? (
        <LoginScreen onLogin={handleLogin} />
      ) : (
        <ChatScreen username={username} onLogout={handleLogout} />
      )}
    </div>
  );
}

export default App;