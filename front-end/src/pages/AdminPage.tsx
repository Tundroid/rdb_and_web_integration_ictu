import React, { useState } from 'react';
import { Container, Row, Col, Nav, NavItem, NavLink, TabContent, TabPane } from 'reactstrap';
import Applicants from '../components/Applicants';
import Admissions from '../components/Admissions';
import Departments from '../components/Departments';
import Programs from '../components/Programs';
import Notifications from '../components/Notifications';

const AdminPage = () => {
  const [activeTab, setActiveTab] = useState('1'); // State to track the active tab

  return (
    <Container fluid>
      <Row>
        <Col sm="2" className="bg-light">
          <h4 className="text-center mt-3">Admin Menu</h4>
          <Nav vertical>
            <NavItem>
              <NavLink
                active={activeTab === '1'}
                onClick={() => setActiveTab('1')}
                style={{
                  cursor: 'pointer',
                  backgroundColor: activeTab === '1' ? '#007bff' : '',
                  color: activeTab === '1' ? '#ffffff' : '',
                }}
              >
                Admissions
              </NavLink>
            </NavItem>
            <NavItem>
              <NavLink
                active={activeTab === '2'}
                onClick={() => setActiveTab('2')}
                style={{
                  cursor: 'pointer',
                  backgroundColor: activeTab === '2' ? '#007bff' : '',
                  color: activeTab === '2' ? '#ffffff' : '',
                }}
              >
                Applicants
              </NavLink>
            </NavItem>
            <NavItem>
              <NavLink
                active={activeTab === '3'}
                onClick={() => setActiveTab('3')}
                style={{
                  cursor: 'pointer',
                  backgroundColor: activeTab === '3' ? '#007bff' : '',
                  color: activeTab === '3' ? '#ffffff' : '',
                }}
              >
                Departments
              </NavLink>
            </NavItem>
            <NavItem>
              <NavLink
                active={activeTab === '4'}
                onClick={() => setActiveTab('4')}
                style={{
                  cursor: 'pointer',
                  backgroundColor: activeTab === '4' ? '#007bff' : '',
                  color: activeTab === '4' ? '#ffffff' : '',
                }}
              >
                Programs
              </NavLink>
            </NavItem>
            <NavItem>
              <NavLink
                active={activeTab === '5'}
                onClick={() => setActiveTab('5')}
                style={{
                  cursor: 'pointer',
                  backgroundColor: activeTab === '5' ? '#007bff' : '',
                  color: activeTab === '5' ? '#ffffff' : '',
                }}
              >
                Notifications
              </NavLink>
            </NavItem>
          </Nav>
        </Col>
        <Col sm="10">
          <TabContent activeTab={activeTab}>
            <TabPane tabId="1">
              <Admissions />
            </TabPane>
            <TabPane tabId="2">
              <Applicants />
            </TabPane>
            <TabPane tabId="3">
              <Departments />
            </TabPane>
            <TabPane tabId="4">
              <Programs />
            </TabPane>
            <TabPane tabId="5">
              <Notifications />
            </TabPane>
          </TabContent>
        </Col>
      </Row>
    </Container>
  );
};

export default AdminPage;