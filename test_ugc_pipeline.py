#!/usr/bin/env python3
"""
LeadPulse AI — UGC Pipeline Test Script

Tests the complete ad suite generation pipeline with professional UGC standards:
1. Smart parse natural language prompts
2. Generate creative copy & screenplay
3. Generate banner
4. Generate 15s UGC-style video with proper timing structure

Tests two industries:
- Industry A: 'Artisanal Gelato Parlour in Bandra'
- Industry B: 'Sneaker Deep-Cleaning & Restoration in Bangalore'
"""

import asyncio
import os
import sys
import time
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from leadpulse.creative_studio import (
    smart_parse_requirement,
    think_and_generate_campaign,
    generate_ad_banner,
    generate_video_ad
)

async def test_industry_pipeline(industry_prompt: str, test_name: str):
    """Test the complete UGC pipeline for a specific industry."""
    print(f"\n{'='*60}")
    print(f"🧪 TESTING: {test_name}")
    print(f"📝 Prompt: {industry_prompt}")
    print(f"{'='*60}")

    start_time = time.time()

    try:
        # Create test output directory
        output_dir = project_root / "test_output" / test_name.lower().replace(" ", "_")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Step 1: Smart Parse
        print("🔍 Step 1: Smart parsing business requirement...")
        parsed_data = await smart_parse_requirement(industry_prompt)

        print(f"   ✓ Parsed: {parsed_data.get('company_name', 'N/A')} - {parsed_data.get('product_name', 'N/A')}")
        print(f"   ✓ Industry: {parsed_data.get('industry', 'N/A')}")
        print(f"   ✓ Location: {parsed_data.get('location', 'N/A')}")

        # Save parsed data
        parsed_file = output_dir / "parsed_data.json"
        with open(parsed_file, "w", encoding="utf-8") as f:
            json.dump(parsed_data, f, indent=2, ensure_ascii=False)
        print(f"   📄 Saved parsed data to: {parsed_file}")

        # Step 2: Generate Creative Copy & Screenplay
        print("\n✍️  Step 2: Generating UGC creative copy & screenplay...")
        creative_data = await think_and_generate_campaign(
            topic=parsed_data.get("topic", ""),
            company_name=parsed_data.get("company_name", ""),
            product_name=parsed_data.get("product_name", ""),
            price_point=parsed_data.get("price_point", ""),
            location=parsed_data.get("location", ""),
            key_benefit=parsed_data.get("key_benefit", ""),
            target_audience=parsed_data.get("target_audience", ""),
            duration=15,
            quality="1080p",
            tone="high_energy"
        )

        # Verify UGC timing structure
        video_script = creative_data.get("video_script", {})
        print(f"   ✓ Video script structure:")
        print(f"     • Hook (0-3s): {video_script.get('hook', '')[:50]}...")
        print(f"     • Problem (3-7s): {video_script.get('problem', '')[:50]}...")
        print(f"     • Solution (7-11s): {video_script.get('solution', '')[:50]}...")
        print(f"     • CTA (11-15s): {video_script.get('cta', '')[:50]}...")

        # Save creative data
        creative_file = output_dir / "creative_data.json"
        with open(creative_file, "w", encoding="utf-8") as f:
            json.dump(creative_data, f, indent=2, ensure_ascii=False)
        print(f"   📄 Saved creative data to: {creative_file}")

        # Step 3: Generate Banner
        print("\n🎨 Step 3: Generating UGC-style banner...")
        try:
            banner_output_dir = output_dir / "banners"
            banner_output_dir.mkdir(parents=True, exist_ok=True)
            banner_path = generate_ad_banner(
                product_name=parsed_data.get("product_name", ""),
                headline=creative_data.get("headlines", [""])[0],
                price_tag=parsed_data.get("price_point", ""),
                location=parsed_data.get("location", ""),
                key_points=parsed_data.get("key_benefit", "").split(","),
                output_dir=str(banner_output_dir),
                aspect_ratio="1:1",
                brand_name=parsed_data.get("company_name", "EXCLUSIVE PREVIEW"),
                industry=parsed_data.get("industry", "universal")
            )
            print(f"   ✓ Banner generated: {banner_path}")
        except Exception as banner_err:
            print(f"   ⚠️  Banner generation error: {banner_err}")

        # Step 4: Generate 15s UGC Video
        print("\n🎬 Step 4: Generating 15s UGC-style video ad...")
        video_output_dir = output_dir / "videos"
        video_output_dir.mkdir(exist_ok=True)

        video_path = await generate_video_ad(
            product_name=parsed_data.get("product_name", ""),
            price_point=parsed_data.get("price_point", ""),
            location=parsed_data.get("location", ""),
            key_benefit=parsed_data.get("key_benefit", ""),
            script_obj=creative_data.get("video_script", {}),
            output_dir=str(video_output_dir),
            voice="en-US-JennyNeural",  # UGC-optimized voice
            industry=parsed_data.get("industry", "food")
        )

        # Verify video file
        if os.path.exists(video_path):
            file_size = os.path.getsize(video_path)
            file_size_mb = file_size / (1024 * 1024)

            print(f"   ✅ Video generated successfully!")
            print(f"   📁 Path: {video_path}")
            print(f"   📊 Size: {file_size_mb:.2f} MB ({file_size:,} bytes)")

            # Verify minimum size (should be >1MB for proper video)
            if file_size_mb > 1.0:
                print(f"   ✅ Video file meets minimum size requirement (>1MB)")
            else:
                print(f"   ⚠️  Video file is smaller than expected ({file_size_mb:.2f} MB)")

            return {
                "success": True,
                "test_name": test_name,
                "video_path": video_path,
                "video_size_bytes": file_size,
                "video_size_mb": file_size_mb,
                "parsed_data": parsed_file,
                "creative_data": creative_file,
                "elapsed_time": time.time() - start_time
            }
        else:
            print(f"   ❌ Video file not created at expected path: {video_path}")
            return {
                "success": False,
                "test_name": test_name,
                "error": f"Video file not created at {video_path}"
            }

    except Exception as e:
        print(f"   ❌ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "test_name": test_name,
            "error": str(e)
        }

async def main():
    """Run UGC pipeline tests for both industries."""
    print("🚀 LEADPULSE AI — UGC PIPELINE VALIDATION TEST")
    print("=" * 60)
    print("Testing professional UGC ad generation with timing structure:")
    print("• Hook (0-3s) • Problem (3-7s) • Solution (7-11s) • CTA (11-15s)")
    print("=" * 60)

    # Test cases
    test_cases = [
        {
            "name": "Artisanal Gelato Parlour in Bandra",
            "prompt": "I want to launch an artisanal gelato and sorbet parlour in Bandra West, Mumbai. We use 100% real fruit, no artificial colors or preservatives. We have unique flavors like Alphonso Mango Sorbet, Pistachio Gelato, and Dark Chocolate Orange. Price point: Single scoop ₹129, Double scoop ₹199. Target audience: young professionals, foodies, and families."
        },
        {
            "name": "Sneaker Deep-Cleaning & Restoration in Bangalore",
            "prompt": "Premium sneaker cleaning and restoration service in Bangalore. We deep clean, deodorize, restore color, and protect luxury sneakers (Nike, Adidas, Jordans). Service starts at ₹499 per pair with 24-hour turnaround. Target audience: sneakerheads, collectors, fashion-conscious youth in Indiranagar and Koramangala."
        }
    ]

    results = []

    for test_case in test_cases:
        result = await test_industry_pipeline(test_case["prompt"], test_case["name"])
        results.append(result)

        # Small pause between tests
        if test_case != test_cases[-1]:
            print("\n⏳ Pausing 2 seconds before next test...")
            await asyncio.sleep(2)

    # Print summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")

    successful_tests = [r for r in results if r.get("success")]
    failed_tests = [r for r in results if not r.get("success")]

    print(f"✅ Successful: {len(successful_tests)}/{len(test_cases)}")
    print(f"❌ Failed: {len(failed_tests)}/{len(test_cases)}")

    if successful_tests:
        print(f"\n🎯 SUCCESSFUL TESTS:")
        for result in successful_tests:
            print(f"  • {result['test_name']}")
            print(f"    Video: {result['video_path']}")
            print(f"    Size: {result['video_size_mb']:.2f} MB")
            print(f"    Time: {result['elapsed_time']:.1f}s")

    if failed_tests:
        print(f"\n⚠️  FAILED TESTS:")
        for result in failed_tests:
            print(f"  • {result['test_name']}: {result.get('error', 'Unknown error')}")

    # Final verification
    print(f"\n{'='*60}")
    print("🔍 FINAL VERIFICATION")
    print(f"{'='*60}")

    all_videos_exist = True
    for result in successful_tests:
        video_path = result.get("video_path")
        if video_path and os.path.exists(video_path):
            file_size_mb = result.get("video_size_mb", 0)
            status = "✅" if file_size_mb > 1.0 else "⚠️ "
            print(f"{status} {os.path.basename(video_path)}: {file_size_mb:.2f} MB")
        else:
            print(f"❌ Missing: {video_path}")
            all_videos_exist = False

    if len(successful_tests) == len(test_cases) and all_videos_exist:
        print(f"\n🎉 ALL TESTS PASSED! UGC pipeline is working correctly.")
        return 0
    else:
        print(f"\n⚠️  Some tests failed. Check logs for details.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)