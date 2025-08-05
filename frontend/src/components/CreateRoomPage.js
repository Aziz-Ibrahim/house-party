import React, { Component } from "react";

export default class CreateRoomPage extends Component {
    constructor(props) {
        super(props);
    }
    render() {
        return (
            <div>
                <h1>Create a New Room</h1>
                <p>Fill in the details to create a new room for your house party.</p>
                {/* Additional form elements can be added here */}
            </div>
        );
    }
}