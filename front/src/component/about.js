import React , {Component} from 'react';
import Heart from '../images/Heart.svg'

class About extends Component {
    render(){
        return(
            <div>
            <div className = 'container'>

                <h1 class= 'Project-Title'>
                    Our Goal
                </h1>

    
                <div className ='row'>
                    <div className = 'col-8'>
                     <h2>To inform those about safe and clean places to dine.</h2>

                            <p>
                                The Health Department has developed an inspection report and scoring system. 
                                After conducting an inspection of the facility, the Health Inspector calculates a score based on the violations observed.
                            </p>
                            <p>
                                Higher Score = <strong>Safer</strong>
                            </p>
                            <p>
                            The contamination of food-contact surfaces.moderate risk category: records specific violations that are of a moderate risk to the public health and safety.low risk category:
                            records violations that are low risk or have no immediate risk to the public health and safety
                            </p>
                        </div>
                        <div className = 'col-4'>
                            <img src = {Heart}/>
                        </div>

                    </div>
            </div>
        </div>
    
        )
    }
}

export default About