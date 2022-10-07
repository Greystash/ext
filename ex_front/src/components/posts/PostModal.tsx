import React from 'react';
import Modal from 'react-bootstrap/Modal';
import { useGlobalState } from '../../state';
import PostForm from './PostForm';


const PostModal = () => {
    const [showPost, setShowPost] = useGlobalState('showNewPost');

    return (
        <Modal
            show={showPost}
            onHide={() => { setShowPost(false) }}>
            <Modal.Header>
                <Modal.Title>
                    Create a new post
                </Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <PostForm />
            </Modal.Body>
        </Modal>
    )
}

export default PostModal;
