import React, { Component } from "react";

export default class Room extends Component {
    constructor(props) {
        super(props);
        this.state = {
            votesToSkip: 2,
            guestCanPause: true,
            isHost: false,
        };
        this.roomCode = this.props.match.params.roomCode;
    }
    
    render() {
        return (
            <div>
                <h3>{this.roomCode}</h3>
                <p>Votes to skip: {this.state.votesToSkip}</p>
                <p>Guest can pause: {this.state.guestCanPause ? "Yes" : "No"}</p>
                <p>Host: {this.state.isHost ? "Yes" : "No"}</p>
            </div>
        );
    }
}