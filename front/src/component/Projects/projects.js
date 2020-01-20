import React, { Component } from 'react';

class Projects extends Component {
    state = {
        isLoaded: false,
        data: null
    };

  componentDidMount() {
      // Call our fetch function below once the component mounts
    this.callBackendAPI()
      .then(res => this.setState({ ...this.state, // spreading in state for future proofing
        isLoaded: true,
        data: res.express }))
      .catch(err => console.log(err));
  }
    // Fetches our GET route from the Express server. (Note the route we are fetching matches the GET route from server.js
  callBackendAPI = async () => {
    const response = await fetch('/db');
    const body = await response.json();
    if (response.status !== 200) {
      throw Error(body.message) 
    }
    return body;
  };

  
    render() {
        console.log(this.state.data)
        const { isLoaded, data } = this.state;
        return(
            <div class = 'Projects'>
                <h1 class = 'Project-Title'>Restaurant Examples</h1>
                  <div className = 'row'>
                  {
                  isLoaded ?
                  data.map((d, index) => {
                      return(
                        
                          <div id='Project' className= 'col' key={index}>
                              <h1>{d.business_name}</h1>
                              <h2>{d.business_address}</h2>
                              <h3>Score : {d.inspection_score}</h3>
                              <h3>{d.risk_category}</h3>
                              <h5>{d.violation_description}</h5>
                          </div>
                         
                      )}  
                  ) : <h1> Loading </h1>
                  }
                 
                  </div>
                 
            </div>
        )
    }
}

export default Projects