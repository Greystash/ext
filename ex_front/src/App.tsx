import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Header from './components/Header';
import AuthModal from './components/auth/AuthModal';
import PostList from './components/posts/PostList';
import PostModal from './components/posts/PostModal';
import UsersModal from './components/auth/UsersModal';

const App = () => (
  <div className="App">
    <Header />
    <AuthModal />
    <PostModal />
    <UsersModal />
    <PostList />
  </div>
)

export default App;
