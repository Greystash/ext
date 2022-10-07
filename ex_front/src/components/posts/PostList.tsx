import React, { useState, useEffect } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Pagination from 'react-bootstrap/Pagination';
import Accordion from 'react-bootstrap/Accordion'
import Row from 'react-bootstrap/Row'
import api from '../../api';
import Post from './Post'
import Badge from 'react-bootstrap/Badge'


interface FiltersT {
    keyword?: string
    date?: Date
    date_gte?: Date
    date_lte?: Date
    tag?: string
    page?: number
}

interface PagesT {
    arr: Array<number>
    total: number
}


const PostList = () => {
    const [filters, setFilters] = useState<FiltersT>({});
    const [posts, setPosts] = useState<Array<PostT>>([]);
    const [pages, setPages] = useState<PagesT>({
        arr: [],
        total: 0,
    });
    const [updated, setUpdated] = useState(false);
    const [tags, setTags] = useState<Array<TagT>>([]);

    useEffect(() => {
        fetchTags()
        fetchPosts()
    }, [])

    useEffect(() => {
        updatePagesArray()
    }, [posts])

    useEffect(() => {
        fetchPosts()
    }, [filters.page])

    const updatePagesArray = () => {
        let pageArray = []
        for (let i = 1; i <= pages.total; i++) {
            pageArray.push(i)
        }
        setPages({ ...pages, arr: pageArray })
    }

    const fetchPosts = () => {
        api.get('posts/', { params: filters })
            .then(res => {
                setPosts(res.data.results)
                setPages({
                    ...pages,
                    total: Math.ceil(res.data.count / 5)
                })
                setUpdated(!updated)
            })
    }

    const handlePageClick = (num: number) => {
        setFilters({ ...filters, page: num })
    }

    const handleSubmit = (e: any) => {
        e.preventDefault()
        setFilters({ ...filters, page: undefined })
        if (filters.page === undefined) {
            fetchPosts()
        }
    }

    const handleFilterChange = (e: any) => {
        const valueName = e.target.name
        const value = e.target.value
        console.log(value)
        setFilters({ ...filters, [valueName]: value })
    }

    const fetchTags = () => {
        api.get('posts/tags/').then(res => {
            setTags(res.data)
        })
    }

    const handleTags = (tag: TagT) => {
        const tagStr = tag.name.concat(',')
        let newTags = filters.tag ? filters.tag.concat(tagStr) : tagStr
        setFilters({ ...filters, tag: newTags })
    }

    return (
        <Container
        >
            {/* Filters */}
            <Row className='mb-5' >
                <Accordion>
                    <Accordion.Item eventKey='0'>
                        <Accordion.Header>Filters</Accordion.Header>
                        <Accordion.Body>
                            <Form onSubmit={handleSubmit}>
                                <Form.Group className="mb-3">
                                    <Form.Label>Search</Form.Label>
                                    <Form.Control
                                        type="text"
                                        placeholder="Enter new post's title"
                                        name='keyword'
                                        onChange={handleFilterChange} />
                                </Form.Group>
                                <Form.Group className="mb-3">
                                    <Form.Label>Date</Form.Label>
                                    <Form.Control
                                        type="date"
                                        placeholder="Enter new post's title"
                                        name='date'
                                        onChange={handleFilterChange} />
                                    <Form.Label>From</Form.Label>
                                    <Form.Control
                                        type="date"
                                        placeholder="Enter new post's title"
                                        name='date__gte'
                                        onChange={handleFilterChange} />
                                    <Form.Label>To</Form.Label>
                                    <Form.Control
                                        type="date"
                                        placeholder="Enter new post's title"
                                        name='date__lte'
                                        onChange={handleFilterChange} />
                                </Form.Group>
                                <Container>
                                    {tags.map(tag => <Badge
                                        className='me-1 mb-1'
                                        key={tag.id}
                                        onClick={() => { handleTags(tag) }}
                                    >
                                        `{tag.name} ({tag.posts_count})`</Badge>)}
                                </Container>
                                <Button type='submit'>Filter</Button>
                            </Form>
                        </Accordion.Body>
                    </Accordion.Item>
                </Accordion>
            </Row>
            {/* Content */}
            <Row md={3}>
                {posts.map(post => <Post key={post.id}  {...post} />)}
            </Row>
            {/* Pagination */}
            <Row md={3}>
                <Pagination>
                    {pages.arr.map(num => <Pagination.Item
                        key={num}
                        onClick={() => {
                            handlePageClick(num)
                        }}
                    >{num}</Pagination.Item>)}
                </Pagination>
            </Row>
        </Container >
    )

}

export default PostList