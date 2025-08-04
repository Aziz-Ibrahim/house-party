import React, { Component } from 'react';
import { render } from 'react-dom';

export default class App extends Component {
    constructor(props) {
        super(props);
    }
    render() {
        return (
            <div>
                <h1>Welcome to the House Party App</h1>
                <p>This is the main application component.</p>
            </div>
        );
    }
}

const appDiv = document.getElementById('app');
render(<App />, appDiv);