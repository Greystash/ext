import React, { useState } from 'react';
import Card from 'react-bootstrap/Card'
import Badge from 'react-bootstrap/Badge'
import { Button } from 'react-bootstrap/lib/InputGroup';


const Post: React.FC<PostT> = (post) => {

    return (
        <Card border='primary' className='me-2 mb-2'>
            <Card.Header>
                By {post.user.username ? post.user.username : 'Moderator'}
            </Card.Header>
            <Card.Body>
                <Card.Title>
                    {post.title}
                </Card.Title>
                <Card.Subtitle>{`Datetime - ${post.datetime}`}</Card.Subtitle>
                <Card.Text>
                    {post.body}
                </Card.Text>
                <Card.Img src={post.image} />
            </Card.Body>
            <Card.Footer>
                {post.tags.map(tag => <Badge
                    key={tag.name}
                    className='me-1'>
                    {tag.name} ({tag.posts_count})
                </Badge>)}
            </Card.Footer>
        </Card >
    )
}

export default Post;