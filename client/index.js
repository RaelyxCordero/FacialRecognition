import React from 'react';
import { render } from 'react-dom';
import MainRouter from './src/components/routes';

const app = document.getElementById('app');

// ReactDOM.render(que voy a renderizar, donde lo haré)
render(<MainRouter />, app);