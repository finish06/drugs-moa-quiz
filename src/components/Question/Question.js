import React from 'react';

import Aux from '../../hoc/Aux'


const question = (props) => {
    return (
        <Aux>
            <h2>What is the mechanism of action of {props.drug}?</h2>
        </Aux>
    )
}

export default question