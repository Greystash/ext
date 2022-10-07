import React, { useState, useEffect } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Badge from 'react-bootstrap/Badge';
import api from '../../api';

interface DataT {
    title?: string
    body?: string
    tags: Array<TagT>
    image?: File
    currentTag?: string
}

const PostForm = () => {
    const [data, setData] = useState<DataT>({
        title: undefined,
        body: undefined,
        currentTag: undefined,
        tags: [],
        image: undefined
    });

    useEffect(() => {
    }, [data.tags, data.currentTag])

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const valueName = e.target.name
        const value = e.target.value
        setData({ ...data, [valueName]: value })
    }

    const handleSubmit = (e: React.SyntheticEvent) => {
        e.preventDefault()
        let formData = new FormData();
        if (data.image) formData.append('image', data.image)
        if (data.title) formData.append('title', data.title)
        if (data.body) formData.append('body', data.body)
        if (data.tags.length > 0) {
            formData.append('raw_tags', JSON.stringify(data.tags))
        }
        api.post('posts/', formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        })
            .catch(e => { console.log(e) })
    }

    const handleTags = (e: any) => {
        if (data.currentTag !== undefined && !data.tags.some(el => el.name === data.currentTag)) {
            setData({ ...data, tags: [...data.tags, { name: data.currentTag }] })
        }
    }

    const handleImageChange = (e: any) => {
        const image = e.target.files[0]
        setData({ ...data, image: image })
    }

    const removeTag = (e: any) => {
        const value = e.target.getAttribute('data-id')
        const idx = data.tags.findIndex(el => el.name === value)
        data.tags.splice(idx, 1)
        setData({ ...data, tags: data.tags })
    }

    return (
        <Form onSubmit={handleSubmit}>
            {/* Title */}
            <Form.Group className="mb-3">
                <Form.Label>Title</Form.Label>
                <Form.Control
                    type="text"
                    placeholder="Enter new post's title"
                    name='title'
                    onChange={handleChange} />
            </Form.Group>
            {/* Body */}
            <Form.Group className="mb-3">
                <Form.Label>Body</Form.Label>
                <Form.Control
                    type="text"
                    as='textarea'
                    placeholder="Enter new post's body"
                    name='body'
                    onChange={handleChange} />
            </Form.Group>
            {/* Tags */}
            <Form.Group className="mb-3">
                <Form.Label>Add tag</Form.Label>
                <Container className='mb-3'>
                    {data.tags?.map(tag => <Badge
                        key={tag.name}
                        data-id={tag.name}
                        data-name='tags'
                        onClick={removeTag}
                        className='me-1'
                    >{tag.name}</Badge>)}
                </Container>
                <Form.Control
                    type="text"
                    placeholder="Enter new tag"
                    name='currentTag'
                    onChange={handleChange} />
                <Button
                    name='tags'
                    onClick={handleTags}
                >Add tag</Button>
            </Form.Group>
            {/* Images */}
            <Form.Group className="mb-3">
                <Form.Label>Select an image</Form.Label>
                <Form.Control
                    onChange={handleImageChange}
                    type="file" size="sm" />
            </Form.Group>
            <Button
                type='submit'
            >Create post</Button>
        </Form>
    )
}

export default PostForm;