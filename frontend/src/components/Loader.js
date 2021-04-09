import React from 'react'
import { Spinner } from 'react-bootstrap'

function Loader() {
    return (
        <Spinner animation="grow" role='status'  variant="success">
            <span className="sr-only">Loading...</span>
        </Spinner>
    )
}

export default Loader
