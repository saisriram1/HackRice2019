import React, { Component } from 'react';
import { BrowserRouter as Router, Route,Switch, Redirect} from 'react-router-dom'
import logo from './logo.svg';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Hello from './Hello.js';
import { Button, Row, Col, Container, Input, Label } from 'reactstrap';

import {
  Collapse,Navbar,NavbarToggler,NavbarBrand,Nav,NavItem,NavLink,UncontrolledDropdown,DropdownToggle,DropdownMenu,DropdownItem } from 'reactstrap';

export default class App extends Component {

constructor(props){
        super(props);

        this.state = {
                query1: "",
                query2: "",
                isOpen: false,
                email: "",
                url: ""
        }
        this.updateInput1 = this.updateInput1.bind(this);
        this.updateInput2 = this.updateInput2.bind(this);
        this.handleEmail = this.handleEmail.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleImage = this.handleImage.bind(this); 
        this.toggle = this.toggle.bind(this);
}

updateInput1(e){
        this.setState({query1: e.target.value});
        console.log(e.target.value);
}

updateInput2(e){
        this.setState({query2: e.target.value});
        console.log(e.target.value);
}

handleEmail(e) {
        this.setState({email: e.target.value});
        console.log(e.target.value);
}

handleImage(e){
        this.setState({url: e.target.value});
        console.log(e.target.value);
}


toggle() {
    this.setState({
      isOpen: !this.state.isOpen
    });
  }

handleSubmit(event) {
        alert("Requests received! picaisso will deliver to your email once its done. :) ");
    const data = {q1:this.state.query1, q2: this.state.query2, email: this.state.email, url: this.state.url};

    fetch('http://10.126.179.87:5000/picaisso/', {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify(data),
    })
      .then(res => res.json())
      .then(res => console.log(res));
  }

render() {
        return (
<div className='App'>
        <Navbar color="light" light expand="md">
                <NavbarBrand href="/"><h1>pic<span className="logo">ai</span>sso.</h1></NavbarBrand>
                <NavbarToggler onClick={this.toggle}/>
                <Collapse isOpen={this.state.isOpen} navbar>
                        <Nav className="ml-auto" navbar>
                                <NavItem>
                                        <NavLink href="/components/">About Us</NavLink>
                                </NavItem>
                                <NavItem>
                                        <NavLink href="https://github.com/saisriram1/HackRice2019">GitHub</NavLink>
                                </NavItem>
                        <UncontrolledDropdown nav inNavbar>
                                <DropdownToggle nav caret>
                                        Options
                                </DropdownToggle>
                                <DropdownMenu right>
                                        <DropdownItem>Option 1</DropdownItem>
                                        <DropdownItem>Option 2</DropdownItem>
                                        <DropdownItem divider />
                                        <DropdownItem>Reset</DropdownItem>
                        </DropdownMenu>
                        </UncontrolledDropdown>
                        </Nav>
                </Collapse>
        </Navbar>

        <Container>
        <h1 className="display-3 mt-5 motto" >Cl<span className="logo">a</span>ss<span className="logo">i</span>fication <span className="logo">simplified.</span></h1>
        <Row>
        <h3 className="question mt-5">Step 1: What do you want to classify?</h3>
        </Row>
        <Row>
          <Col><Input placeholder="Class one name." className="mt-5" onChange= {this.updateInput1}/></Col>
          <Col><Input placeholder= "Class two name." className="mt-5" onChange={this.updateInput2}/></Col>
        </Row>
        <Row>
        <h3 className=" question mt-5">Step 2: We will send the results to your email</h3>
        </Row>
        <Row>
        <Col></Col>
        <Col><Input placeholder="Enter email" onChange={this.handleEmail} className="mt-5"></Input></Col>
        <Col></Col>
        </Row>
        <Row>
        <h3 className=" question mt-5">Test <span className="logo">picaisso</span> with an image of your choice</h3>
        </Row>
        <Row>
        <Col></Col>
        <Col><Input className="mt-5" placeholder="URL of image" size="lg" onChange={this.handleImage}></Input></Col>
        <Col></Col>
        </Row>
        <Row>
        <Col></Col>
        <Col><Button className="mt-5" color="danger" size="lg" onClick={this.handleSubmit}>Go</Button></Col>
        <Col></Col>
        </Row>
      </Container>
        </div>
);
        }
}
