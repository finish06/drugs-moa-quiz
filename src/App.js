import React from 'react';
import logo from './logo.svg';
import './App.css';

import Layout from './components/Layout/Layout'
import Questionaire from './containers/Questionaire/Questionaire'


function App() {
  return (
    <Layout>
      <Questionaire></Questionaire>
    </Layout>
  );
}

export default App;
