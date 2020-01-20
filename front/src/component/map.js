import React, {Component} from 'react'
import GoogleMapReact from 'google-map-react'


class Map extends Component{
    static defaultProps = {
        center: {
          lat: 59.95,
          lng: 30.33
        },
        zoom: 11
      };
        
    render() {
        return (
            // Important! Always set the container height explicitly
            <div style={{ height: '100vh', width: '100%' }}>
            <GoogleMapReact
               ref={(el) => this._googleMap = el}          
               bootstrapURLKeys={{ key: "AIzaSyCtn9i2oi7bB7_rYWLaQ2z3yzCUvEocUmQ" }}          
               defaultCenter={this.props.center}          
               defaultZoom={this.props.zoom}          
               heatmapLibrary={true}          
            >
             
            </GoogleMapReact>
            </div>
        );
    }
}


export default Map