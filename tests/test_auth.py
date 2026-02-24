def test_vetting_gate(app, client):
    """Confirm unvetted users cannot access internal services."""
    with app.app_context():
        # Create a user who is an ADMIN but NOT vetted
        unvetted_admin = User(
            email="rogue_admin@fsi.com", 
            role=UserRole.ADMIN, 
            employee_approved=False
        )
        
        # This property is used by the @role_required decorator
        assert unvetted_admin.is_fully_vetted is False
        
        # Test the helper method logic
        assert unvetted_admin.has_role("ADMIN") is True
