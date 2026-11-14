"""
Populate the local database with realistic lead records and full WhatsApp chat transcripts.
"""
import asyncio
import uuid
from datetime import datetime, timezone
from sqlalchemy import select

from leadpulse.database import async_session_factory, Tenant, Project, Lead, Message, LeadStatus, LeadSource, MessageDirection

async def seed():
    async with async_session_factory() as session:
        t_stmt = select(Tenant).limit(1)
        res = await session.execute(t_stmt)
        tenant = res.scalar_one_or_none()
        if not tenant:
            print("No tenant found. Run seed_demo.py first.")
            return

        p_stmt = select(Project).where(Project.tenant_id == tenant.id).limit(1)
        res = await session.execute(p_stmt)
        project = res.scalar_one_or_none()
        if not project:
            print("No project found. Run seed_demo.py first.")
            return

        # Lead 1: Hot Qualified Lead
        lead1 = Lead(
            id=uuid.uuid4(),
            tenant_id=tenant.id,
            project_id=project.id,
            phone_number="+919820199999",
            name="Vikramaditya Sharma",
            status=LeadStatus.appointment_booked,
            lead_score=94,
            source=LeadSource.ctwa,
            qualification_data={
                "budget": "₹95 Lakhs",
                "unit_type": "3BHK Luxury",
                "timeline": "Ready to move in 3 months",
                "site_visit_slot": "Saturday, 11:30 AM",
                "payment_mode": "Self-financed + HDFC Bank loan"
            },
            created_at=datetime.now(timezone.utc),
            qualified_at=datetime.now(timezone.utc)
        )
        session.add(lead1)
        await session.flush()

        m1_1 = Message(id=uuid.uuid4(), lead_id=lead1.id, tenant_id=tenant.id, direction=MessageDirection.inbound, content="Hi! Saw your Instagram ad for Greenfield Signature. Interested in 3BHK.")
        m1_2 = Message(id=uuid.uuid4(), lead_id=lead1.id, tenant_id=tenant.id, direction=MessageDirection.outbound, content="Namaste Vikramaditya! Welcome to Greenfield Signature. Our 3BHK luxury units start from ₹85 Lakhs. Does that match your planned budget?")
        m1_3 = Message(id=uuid.uuid4(), lead_id=lead1.id, tenant_id=tenant.id, direction=MessageDirection.inbound, content="Yes, my budget is around ₹95 Lakhs. Looking to move in before Diwali.")
        m1_4 = Message(id=uuid.uuid4(), lead_id=lead1.id, tenant_id=tenant.id, direction=MessageDirection.outbound, content="Wonderful! We have fully furnished sample flats open for private viewing this weekend. Would Saturday 11:30 AM or 3:30 PM suit you better?")
        m1_5 = Message(id=uuid.uuid4(), lead_id=lead1.id, tenant_id=tenant.id, direction=MessageDirection.inbound, content="Saturday 11:30 AM works perfectly. Please send the gate pass.")
        m1_6 = Message(id=uuid.uuid4(), lead_id=lead1.id, tenant_id=tenant.id, direction=MessageDirection.outbound, content="Confirmed! We have reserved your 11:30 AM VIP slot. Our sales head will call you shortly with the exact Google Maps location pin.")

        # Lead 2: In Conversation
        lead2 = Lead(
            id=uuid.uuid4(),
            tenant_id=tenant.id,
            project_id=project.id,
            phone_number="+919876543210",
            name="Ananya Deshmukh",
            status=LeadStatus.in_conversation,
            lead_score=78,
            source=LeadSource.ctwa,
            qualification_data={
                "budget": "₹88 Lakhs",
                "unit_type": "2BHK",
                "timeline": "Exploring within 6 months"
            },
            created_at=datetime.now(timezone.utc)
        )
        session.add(lead2)
        await session.flush()

        m2_1 = Message(id=uuid.uuid4(), lead_id=lead2.id, tenant_id=tenant.id, direction=MessageDirection.inbound, content="Hello, can you share the floor plan for 2BHK?")
        m2_2 = Message(id=uuid.uuid4(), lead_id=lead2.id, tenant_id=tenant.id, direction=MessageDirection.outbound, content="Hello Ananya! Happy to assist. Our 2BHK spacious residences start at ₹85 Lakhs. Does this align with your budget?")
        m2_3 = Message(id=uuid.uuid4(), lead_id=lead2.id, tenant_id=tenant.id, direction=MessageDirection.inbound, content="Yes, around ₹85-90L is fine. Is there a clubhouse and swimming pool?")

        # Lead 3: Disqualified (Low Budget)
        lead3 = Lead(
            id=uuid.uuid4(),
            tenant_id=tenant.id,
            project_id=project.id,
            phone_number="+919123456789",
            name="Rajesh Gupta",
            status=LeadStatus.disqualified,
            disqualification_reason="Budget below minimum project threshold (₹35L vs ₹85L min)",
            lead_score=22,
            source=LeadSource.ctwa,
            qualification_data={"budget": "₹35 Lakhs"},
            created_at=datetime.now(timezone.utc)
        )
        session.add(lead3)
        await session.flush()

        m3_1 = Message(id=uuid.uuid4(), lead_id=lead3.id, tenant_id=tenant.id, direction=MessageDirection.inbound, content="Need flat in this area.")
        m3_2 = Message(id=uuid.uuid4(), lead_id=lead3.id, tenant_id=tenant.id, direction=MessageDirection.outbound, content="Namaste Rajesh! Our premium towers start at ₹85 Lakhs. Does that fit your planned budget?")
        m3_3 = Message(id=uuid.uuid4(), lead_id=lead3.id, tenant_id=tenant.id, direction=MessageDirection.inbound, content="No my max budget is 35 lakhs only for 1bhk.")
        m3_4 = Message(id=uuid.uuid4(), lead_id=lead3.id, tenant_id=tenant.id, direction=MessageDirection.outbound, content="Understood! Our current phase has 2 & 3BHKs starting at ₹85L. We have noted your details and will notify you if affordable units open in Phase 2.")

        session.add_all([m1_1, m1_2, m1_3, m1_4, m1_5, m1_6, m2_1, m2_2, m2_3, m3_1, m3_2, m3_3, m3_4])
        await session.commit()
        print("Successfully seeded 3 realistic leads with complete conversation histories!")

if __name__ == "__main__":
    asyncio.run(seed())
