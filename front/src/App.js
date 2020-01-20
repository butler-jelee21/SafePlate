import React from 'react';
import './App.css';

import Banner from './component/banner/banner'
import Projects from './component/Projects/projects'
import FooterPagePro from './component/footer/footer'
import About from './component/about'
import Map from './component/map'



function App() {
  return (
    <div className="App">
      <Banner />
      <Map />
      <About />
      <Projects />      
      <FooterPagePro />
    </div>
  );
}

export default App;
