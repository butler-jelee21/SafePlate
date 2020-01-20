import React from "react";
import './styles.css'

const FooterPagePro = () => {
  return (
    <div>
        <div className="footer-copyright text-center py-3">
            <a className="tw-ic" href="mailto:wujeffrey567@gmail.com" target="_blank">
                <i className="fas fa-envelope fa-lg white-text fa-2x"/>
            </a>
            <a className="gplus-ic" href='https://github.com/jeffrey856' target="_blank">
                <i className="fab fa-github fa-lg white-text  fa-2x" />
            </a>
            <a className="li-ic" href='https://www.linkedin.com/in/jeffrey-wu99/' target="_blank">
                <i className="fab fa-linkedin-in fa-lg white-text fa-2x" />
            </a>
           
        </div>
        <div className="footer-copyright text-center py-3">
          &copy; {new Date().getFullYear()} :{" "}
          <a> SafePlate </a>
      </div>
    </div>
    
  
  );
}

export default FooterPagePro;