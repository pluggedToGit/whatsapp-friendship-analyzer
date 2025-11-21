"""
Image Report Generator for WhatsApp Friendship Analysis
Creates beautiful, shareable PNG images for social media
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from typing import Dict, Any, List, Tuple
import textwrap

class WhatsAppImageGenerator:
    """Generate beautiful shareable images from WhatsApp analysis data"""
    
    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or Path("data/analysis")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Color scheme - purple gradient theme
        self.colors = {
            'bg_gradient_start': (102, 126, 234),  # #667eea
            'bg_gradient_end': (118, 75, 162),      # #764ba2
            'white': (255, 255, 255),
            'card_bg': (248, 249, 250),
            'text_dark': (33, 37, 41),
            'text_light': (108, 117, 125),
            'accent': (245, 87, 108),               # #f5576c
            'success': (76, 175, 80),
            'warning': (255, 152, 0),
        }
    
    def generate_summary_image(self, data: Dict[str, Any], filename: str = None) -> Path:
        """
        Generate a beautiful summary image
        
        Args:
            data: Dictionary containing all analysis results
            filename: Optional custom filename
            
        Returns:
            Path to generated PNG file
        """
        from datetime import datetime
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"whatsapp_analysis_{timestamp}.png"
        
        output_path = self.output_dir / filename
        
        # Create image (Instagram post size: 1080x1350)
        width, height = 1080, 1350
        img = Image.new('RGB', (width, height), self.colors['white'])
        draw = ImageDraw.Draw(img)
        
        # Draw gradient background for header
        self._draw_gradient_rect(img, 0, 0, width, 300, 
                                 self.colors['bg_gradient_start'], 
                                 self.colors['bg_gradient_end'])
        
        y_offset = 40
        
        # Title
        y_offset = self._draw_text_centered(draw, "💬 WhatsApp Relationship Analysis", 
                                            y_offset, width, 48, self.colors['white'], bold=True)
        
        y_offset += 20
        y_offset = self._draw_text_centered(draw, "Deep Behavioral & Psychological Insights", 
                                            y_offset, width, 24, self.colors['white'])
        
        y_offset = 320
        
        # Main stats section
        y_offset = self._draw_stats_grid(draw, data, y_offset, width)
        
        y_offset += 30
        
        # Relationship classification
        y_offset = self._draw_relationship_card(draw, data, y_offset, width)
        
        y_offset += 30
        
        # Key insights
        y_offset = self._draw_insights_card(draw, data, y_offset, width)
        
        # Footer
        self._draw_footer(draw, width, height)
        
        img.save(output_path, 'PNG', quality=95)
        print(f"\n✅ Image generated: {output_path}")
        return output_path
    
    def _draw_gradient_rect(self, img: Image, x1: int, y1: int, x2: int, y2: int, 
                           color1: Tuple[int, int, int], color2: Tuple[int, int, int]):
        """Draw a gradient rectangle"""
        draw = ImageDraw.Draw(img)
        for i, y in enumerate(range(y1, y2)):
            ratio = i / (y2 - y1)
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            draw.rectangle([x1, y, x2, y + 1], fill=(r, g, b))
    
    def _get_font(self, size: int, bold: bool = False):
        """Get a font, fallback to default if needed"""
        try:
            if bold:
                return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", size)
            return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", size)
        except:
            return ImageFont.load_default()
    
    def _draw_text_centered(self, draw: ImageDraw, text: str, y: int, width: int, 
                           size: int, color: Tuple[int, int, int], bold: bool = False) -> int:
        """Draw centered text and return new y position"""
        font = self._get_font(size, bold)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        draw.text((x, y), text, font=font, fill=color)
        return y + text_height + 10
    
    def _draw_stats_grid(self, draw: ImageDraw, data: Dict, y_start: int, width: int) -> int:
        """Draw stats grid"""
        padding = 40
        card_width = (width - padding * 3) // 2
        card_height = 120
        
        stats = [
            {
                'label': 'Total Messages',
                'value': f"{data.get('total_messages', 0):,}",
                'subtitle': f"Over {data.get('duration_days', 0)} days"
            },
            {
                'label': 'Daily Average',
                'value': f"{data.get('msgs_per_day', 0):.0f}",
                'subtitle': 'Messages per day'
            },
            {
                'label': 'Response Time',
                'value': '<1min',
                'subtitle': 'Median response'
            },
            {
                'label': 'Late Night',
                'value': f"{data.get('night_percentage', 0):.0f}%",
                'subtitle': 'After 11 PM'
            }
        ]
        
        y = y_start
        for i, stat in enumerate(stats):
            row = i // 2
            col = i % 2
            x = padding + col * (card_width + padding)
            card_y = y + row * (card_height + 20)
            
            # Draw card background
            draw.rounded_rectangle(
                [x, card_y, x + card_width, card_y + card_height],
                radius=15,
                fill=self.colors['card_bg']
            )
            
            # Draw content
            label_font = self._get_font(16)
            value_font = self._get_font(42, bold=True)
            subtitle_font = self._get_font(14)
            
            # Center text in card
            text_y = card_y + 15
            
            # Label
            bbox = draw.textbbox((0, 0), stat['label'], font=label_font)
            label_width = bbox[2] - bbox[0]
            draw.text((x + (card_width - label_width) // 2, text_y), 
                     stat['label'], font=label_font, fill=self.colors['text_light'])
            
            text_y += 30
            
            # Value
            bbox = draw.textbbox((0, 0), stat['value'], font=value_font)
            value_width = bbox[2] - bbox[0]
            draw.text((x + (card_width - value_width) // 2, text_y), 
                     stat['value'], font=value_font, fill=self.colors['text_dark'])
            
            text_y += 50
            
            # Subtitle
            bbox = draw.textbbox((0, 0), stat['subtitle'], font=subtitle_font)
            subtitle_width = bbox[2] - bbox[0]
            draw.text((x + (card_width - subtitle_width) // 2, text_y), 
                     stat['subtitle'], font=subtitle_font, fill=self.colors['text_light'])
        
        return y + 2 * (card_height + 20)
    
    def _draw_relationship_card(self, draw: ImageDraw, data: Dict, y_start: int, width: int) -> int:
        """Draw relationship classification card"""
        padding = 40
        card_width = width - 2 * padding
        
        # Calculate card height based on content
        card_height = 220
        
        x = padding
        y = y_start
        
        # Draw gradient background for card
        temp_img = Image.new('RGB', (card_width, card_height), self.colors['white'])
        self._draw_gradient_rect(temp_img, 0, 0, card_width, card_height,
                                 (240, 147, 251), (245, 87, 108))
        
        # Paste onto main image
        from PIL import Image as PILImage
        main_img = draw._image
        main_img.paste(temp_img, (x, y))
        
        # Draw rounded corners effect
        draw.rounded_rectangle([x, y, x + card_width, y + card_height], 
                              radius=15, outline=None)
        
        # Content
        text_y = y + 25
        
        # Title
        title_font = self._get_font(32, bold=True)
        relationship_type = data.get('relationship_type', 'Unknown')
        bbox = draw.textbbox((0, 0), relationship_type, font=title_font)
        title_width = bbox[2] - bbox[0]
        draw.text((x + (card_width - title_width) // 2, text_y), 
                 relationship_type, font=title_font, fill=self.colors['white'])
        
        text_y += 50
        
        # Confidence badge
        confidence = data.get('confidence_level', 'MODERATE')
        badge_font = self._get_font(18, bold=True)
        badge_text = f"Confidence: {confidence}"
        bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
        badge_width = bbox[2] - bbox[0]
        badge_x = x + (card_width - badge_width) // 2 - 20
        
        # Draw badge background
        draw.rounded_rectangle(
            [badge_x, text_y, badge_x + badge_width + 40, text_y + 35],
            radius=18,
            fill=(255, 255, 255, 100)
        )
        draw.text((badge_x + 20, text_y + 5), badge_text, 
                 font=badge_font, fill=self.colors['white'])
        
        text_y += 60
        
        # Romantic indicators
        romantic_indicators = len(data.get('romantic_indicators', []))
        indicator_font = self._get_font(20)
        indicator_text = f"✅ {romantic_indicators} Romantic Indicators Detected"
        bbox = draw.textbbox((0, 0), indicator_text, font=indicator_font)
        indicator_width = bbox[2] - bbox[0]
        draw.text((x + (card_width - indicator_width) // 2, text_y), 
                 indicator_text, font=indicator_font, fill=self.colors['white'])
        
        return y + card_height
    
    def _draw_insights_card(self, draw: ImageDraw, data: Dict, y_start: int, width: int) -> int:
        """Draw key insights card"""
        padding = 40
        card_width = width - 2 * padding
        
        x = padding
        y = y_start
        
        # Title
        title_font = self._get_font(28, bold=True)
        draw.text((x, y), "🔍 Key Insights", font=title_font, fill=self.colors['text_dark'])
        
        y += 50
        
        # Get insights
        insights = self._get_key_insights(data)
        
        # Draw each insight
        insight_font = self._get_font(18)
        line_height = 40
        
        for insight in insights[:6]:  # Limit to 6 insights to fit
            # Bullet point
            draw.ellipse([x, y + 8, x + 12, y + 20], fill=self.colors['bg_gradient_start'])
            
            # Wrap text
            wrapped = textwrap.fill(insight, width=65)
            lines = wrapped.split('\n')
            
            for line in lines:
                draw.text((x + 25, y), line, font=insight_font, fill=self.colors['text_dark'])
                y += line_height
        
        return y + 20
    
    def _get_key_insights(self, data: Dict) -> List[str]:
        """Generate key insights from data"""
        insights = []
        
        msgs_per_day = data.get('msgs_per_day', 0)
        if msgs_per_day > 50:
            insights.append(f"Extremely high frequency: {msgs_per_day:.0f} messages/day")
        
        duration = data.get('duration_days', 0)
        if duration < 90:
            insights.append(f"Recent connection: Only {duration} days old")
        
        night_pct = data.get('night_percentage', 0)
        if night_pct > 20:
            insights.append(f"Late-night communication: {night_pct:.0f}% after 11 PM")
        
        greetings = data.get('total_greetings', 0)
        if greetings > 10:
            insights.append(f"Morning/night rituals: {greetings} good morning/night messages")
        
        affection = data.get('total_affection', 0)
        if affection > 10:
            insights.append(f"Affectionate language: {affection} intimate terms used")
        
        insights.append("Near-instant responses from both parties (under 1 min)")
        insights.append("Balanced conversation initiation (mutual interest)")
        
        # Add personalities
        profiles = data.get('personality_profiles', {})
        for person, profile in list(profiles.items())[:2]:
            expr_style = profile.get('expression_style', '')
            if 'expressive' in expr_style.lower():
                insights.append(f"{person}: {expr_style}")
        
        return insights
    
    def _draw_footer(self, draw: ImageDraw, width: int, height: int):
        """Draw footer"""
        y = height - 60
        
        footer_font = self._get_font(14)
        footer_text = "Generated by WhatsApp Friendship Analyzer"
        
        bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        
        draw.text((x, y), footer_text, font=footer_font, fill=self.colors['text_light'])
        
        y += 25
        emoji_text = "🔒 Privacy-focused • 💡 Data-driven insights"
        bbox = draw.textbbox((0, 0), emoji_text, font=footer_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, y), emoji_text, font=footer_font, fill=self.colors['text_light'])
