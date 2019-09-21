import React, { Component } from 'react';
import { BrowserRouter as Router, Route,Switch, Redirect} from 'react-router-dom'
import logo from './logo.svg';
import './App.css';
import Hello from './Hello.js';
import 'bootstrap/dist/css/bootstrap.min.css';
import Button from 'react-bootstrap/Button';

class App extends Component {

  getTeams = _ => {
    fetch('http://localhost:3000')
    .then(response => response.json())
    .catch(err => console.error(err))
  }

route_path = () => {
          this.props.history.push('/hello');
  }

  renderTeam = ({id, name, description}) => <div key={id}>{name}</div>
  render() {
    return (
      <div className="App">
      <div className= "fields">
        <div>
        <input/>
        </div>
        <div>
        <input/>
        </div>
      </div>
      <button variant="primary" onClick={this.route_path}>"We're here"</button>
      <Route path="/hello" component={Hello}/>
      </div>
    );
  }
}

export default () => (
        <div>
                <Router>
                        <Route component={App} />
                </Router>
        </div>

);
