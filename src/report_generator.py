"""
HTML Report Generator for WhatsApp Friendship Analysis
Creates beautiful, shareable HTML reports with charts and insights
"""

from datetime import datetime
from pathlib import Path
import json
from typing import Dict, List, Any
import base64

class WhatsAppReportGenerator:
    """Generate beautiful HTML reports from WhatsApp analysis data"""
    
    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or Path("data/analysis")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_report(self, analysis_data: Dict[str, Any], filename: str = None) -> Path:
        """
        Generate a comprehensive HTML report
        
        Args:
            analysis_data: Dictionary containing all analysis results
            filename: Optional custom filename
            
        Returns:
            Path to generated HTML file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"whatsapp_analysis_report_{timestamp}.html"
        
        output_path = self.output_dir / filename
        
        html_content = self._generate_html(analysis_data)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n✅ Report generated: {output_path}")
        return output_path
    
    def generate_compact_card(self, analysis_data: Dict[str, Any], filename: str = None) -> Path:
        """
        Generate a compact, single-page card format report
        
        Args:
            analysis_data: Dictionary containing all analysis results
            filename: Optional custom filename
            
        Returns:
            Path to generated compact HTML file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"whatsapp_card_{timestamp}.html"
        
        output_path = self.output_dir / filename
        
        html_content = self._generate_compact_html(analysis_data)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n✅ Compact card generated: {output_path}")
        return output_path
    
    def _generate_html(self, data: Dict[str, Any]) -> str:
        """Generate the complete HTML document"""
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WhatsApp Relationship Analysis Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .header .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
            border-bottom: 2px solid #f0f0f0;
            padding-bottom: 30px;
        }}
        
        .section:last-child {{
            border-bottom: none;
        }}
        
        .section-title {{
            font-size: 2em;
            color: #667eea;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 5px;
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .stat-description {{
            font-size: 0.85em;
            opacity: 0.8;
        }}
        
        .participant-card {{
            background: #f8f9fa;
            border-left: 5px solid #667eea;
            padding: 20px;
            margin: 15px 0;
            border-radius: 10px;
        }}
        
        .participant-name {{
            font-size: 1.5em;
            color: #667eea;
            font-weight: bold;
            margin-bottom: 15px;
        }}
        
        .trait {{
            display: flex;
            align-items: center;
            margin: 10px 0;
            font-size: 1.05em;
        }}
        
        .trait-icon {{
            margin-right: 10px;
            font-size: 1.3em;
        }}
        
        .judgment-box {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin: 20px 0;
            box-shadow: 0 10px 30px rgba(245, 87, 108, 0.3);
        }}
        
        .judgment-title {{
            font-size: 1.8em;
            font-weight: bold;
            margin-bottom: 15px;
            text-align: center;
        }}
        
        .judgment-content {{
            font-size: 1.1em;
            line-height: 1.8;
        }}
        
        .indicator-list {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 15px 0;
        }}
        
        .indicator-item {{
            display: flex;
            align-items: flex-start;
            margin: 12px 0;
            padding: 10px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
        
        .indicator-number {{
            background: #667eea;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 15px;
            flex-shrink: 0;
        }}
        
        .progress-bar {{
            background: #e9ecef;
            height: 30px;
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
        }}
        
        .progress-fill {{
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            transition: width 1s ease;
        }}
        
        .score-badge {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            margin: 5px;
        }}
        
        .timeline {{
            position: relative;
            padding-left: 30px;
            margin: 20px 0;
        }}
        
        .timeline::before {{
            content: '';
            position: absolute;
            left: 10px;
            top: 0;
            bottom: 0;
            width: 3px;
            background: #667eea;
        }}
        
        .timeline-item {{
            position: relative;
            margin: 20px 0;
            padding: 15px 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }}
        
        .timeline-item::before {{
            content: '';
            position: absolute;
            left: -24px;
            top: 20px;
            width: 15px;
            height: 15px;
            border-radius: 50%;
            background: #667eea;
            border: 3px solid white;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 30px;
            text-align: center;
            color: #666;
        }}
        
        .emoji-large {{
            font-size: 3em;
            text-align: center;
            margin: 20px 0;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .container {{
                box-shadow: none;
            }}
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8em;
            }}
            
            .stat-grid {{
                grid-template-columns: 1fr;
            }}
            
            .content {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💬 WhatsApp Relationship Analysis</h1>
            <div class="subtitle">Deep Behavioral & Psychological Insights</div>
            <div class="subtitle" style="margin-top: 10px; opacity: 0.7;">
                Generated on {datetime.now().strftime("%B %d, %Y at %I:%M %p")}
            </div>
        </div>
        
        <div class="content">
            {self._generate_overview_section(data)}
            {self._generate_relationship_classification(data)}
            {self._generate_communication_analysis(data)}
            {self._generate_personality_profiles(data)}
            {self._generate_behavioral_indicators(data)}
            {self._generate_final_judgment(data)}
        </div>
        
        <div class="footer">
            <p>🔒 This analysis is based on statistical patterns and behavioral psychology.</p>
            <p style="margin-top: 10px;">Generated by WhatsApp Friendship Analyzer</p>
        </div>
    </div>
</body>
</html>"""
    
    def _generate_overview_section(self, data: Dict) -> str:
        """Generate overview statistics section"""
        participants = data.get('participants', [])
        total_messages = data.get('total_messages', 0)
        duration_days = data.get('duration_days', 0)
        msgs_per_day = data.get('msgs_per_day', 0)
        
        return f"""
        <div class="section">
            <div class="section-title">📊 Overview Statistics</div>
            
            <div class="stat-grid">
                <div class="stat-card">
                    <div class="stat-label">Participants</div>
                    <div class="stat-value">{len(participants)}</div>
                    <div class="stat-description">{', '.join(participants)}</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-label">Total Messages</div>
                    <div class="stat-value">{total_messages:,}</div>
                    <div class="stat-description">Over {duration_days} days</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-label">Daily Average</div>
                    <div class="stat-value">{msgs_per_day:.0f}</div>
                    <div class="stat-description">Messages per day</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-label">Response Time</div>
                    <div class="stat-value">&lt;1min</div>
                    <div class="stat-description">Median response time</div>
                </div>
            </div>
        </div>
        """
    
    def _generate_relationship_classification(self, data: Dict) -> str:
        """Generate relationship type classification section"""
        relationship_type = data.get('relationship_type', 'Unknown')
        confidence = data.get('confidence_level', 'MODERATE')
        relationship_scores = data.get('relationship_scores', {})
        relationship_type_map = data.get('relationship_type_map', {})
        
        confidence_color = {
            'VERY HIGH': '#4caf50',
            'HIGH': '#66bb6a',
            'MODERATE': '#ff9800',
            'LOW': '#f44336'
        }.get(confidence, '#999')
        
        # Get emoji for relationship type
        emoji_map = {
            'romantic': '💕',
            'close_friends': '👥',
            'casual_friends': '🤝',
            'family_sibling': '👨‍👩‍👧‍👦',
            'family_parent': '👨‍👩‍👧',
            'colleagues': '💼',
            'work_professional': '🏢',
            'boss_subordinate': '👔',
            'acquaintances': '👋',
            'enemy_conflict': '⚔️',
            'new_acquaintance': '✨',
        }
        
        # Generate progress bars for top 5 relationship types
        relationship_bars_html = ""
        if relationship_scores and relationship_type_map:
            # Sort by score descending
            sorted_scores = sorted(relationship_scores.items(), key=lambda x: x[1], reverse=True)[:5]
            max_score = max(relationship_scores.values()) if relationship_scores else 100
            
            for rel_key, score in sorted_scores:
                rel_name = relationship_type_map.get(rel_key, rel_key)
                # Get emoji for this type
                emoji = next((v for k, v in emoji_map.items() if k in rel_key), '🔹')
                percentage = (score / max(max_score, 1)) * 100
                
                relationship_bars_html += f"""
                <div style="margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span>{emoji} {rel_name}</span>
                        <span>{score}/{max_score}</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {percentage}%">
                            {percentage:.0f}%
                        </div>
                    </div>
                </div>
                """
        else:
            # Fallback to old romantic score display
            romantic_score = data.get('romantic_score', 0)
            relationship_bars_html = f"""
            <div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>💕 Romantic/Dating</span>
                    <span>{romantic_score}/200</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {(romantic_score/200)*100}%">
                        {(romantic_score/200)*100:.0f}%
                    </div>
                </div>
            </div>
            """
        
        return f"""
        <div class="section">
            <div class="section-title">💑 Relationship Classification</div>
            
            <div class="judgment-box">
                <div class="judgment-title">
                    {relationship_type}
                </div>
                <div style="text-align: center; margin: 20px 0;">
                    <span class="score-badge" style="background: {confidence_color}; font-size: 1.2em;">
                        Confidence: {confidence}
                    </span>
                </div>
                <div class="judgment-content" style="text-align: center;">
                    {data.get('relationship_interpretation', 'Analysis based on communication patterns and behavioral indicators.')}
                </div>
            </div>
            
            <div style="margin-top: 30px;">
                <h3 style="margin-bottom: 15px;">Relationship Type Probability Scores</h3>
                {relationship_bars_html}
            </div>
        </div>
        """
    
    def _generate_communication_analysis(self, data: Dict) -> str:
        """Generate communication patterns section"""
        message_counts = data.get('message_counts', {})
        conversation_starts = data.get('conversation_starts', {})
        
        return f"""
        <div class="section">
            <div class="section-title">💬 Communication Patterns</div>
            
            <div class="stat-grid">
                {self._generate_message_distribution(message_counts)}
                {self._generate_initiation_stats(conversation_starts)}
                {self._generate_response_stats(data)}
            </div>
            
            <div style="margin-top: 30px;">
                <h3>⏰ Key Communication Metrics</h3>
                <div class="timeline">
                    {self._generate_timeline_items(data)}
                </div>
            </div>
        </div>
        """
    
    def _generate_message_distribution(self, message_counts: Dict) -> str:
        """Generate message distribution cards"""
        total = sum(message_counts.values()) if message_counts else 1
        cards = ""
        
        for person, count in message_counts.items():
            percentage = (count / total) * 100
            cards += f"""
                <div class="stat-card">
                    <div class="stat-label">{person}</div>
                    <div class="stat-value">{count}</div>
                    <div class="stat-description">{percentage:.1f}% of messages</div>
                </div>
            """
        
        return cards
    
    def _generate_initiation_stats(self, conversation_starts: Dict) -> str:
        """Generate conversation initiation stats"""
        if not conversation_starts:
            return ""
        
        total = sum(conversation_starts.values())
        cards = ""
        
        for person, count in conversation_starts.items():
            percentage = (count / total) * 100
            cards += f"""
                <div class="stat-card">
                    <div class="stat-label">{person} Initiated</div>
                    <div class="stat-value">{count}</div>
                    <div class="stat-description">{percentage:.1f}% of conversations</div>
                </div>
            """
        
        return cards
    
    def _generate_response_stats(self, data: Dict) -> str:
        """Generate response time statistics"""
        response_times = data.get('response_times_by_person', {})
        cards = ""
        
        for person, times in response_times.items():
            if times:
                import statistics
                avg = statistics.mean(times)
                cards += f"""
                    <div class="stat-card">
                        <div class="stat-label">{person} Response</div>
                        <div class="stat-value">{avg:.0f}m</div>
                        <div class="stat-description">Average response time</div>
                    </div>
                """
        
        return cards
    
    def _generate_timeline_items(self, data: Dict) -> str:
        """Generate timeline items for key metrics"""
        items = ""
        
        # Late night messaging
        night_pct = data.get('night_percentage', 0)
        items += f"""
            <div class="timeline-item">
                <strong>🌙 Late-Night Communication:</strong> {night_pct:.1f}% of messages sent after 11 PM
            </div>
        """
        
        # Greetings
        greetings = data.get('total_greetings', 0)
        items += f"""
            <div class="timeline-item">
                <strong>☀️ Good Morning/Night Rituals:</strong> {greetings} instances detected
            </div>
        """
        
        # Affectionate language
        affection = data.get('total_affection', 0)
        items += f"""
            <div class="timeline-item">
                <strong>❤️ Affectionate Language:</strong> {affection} instances of intimate terms
            </div>
        """
        
        return items
    
    def _generate_personality_profiles(self, data: Dict) -> str:
        """Generate personality profiles for participants"""
        profiles = data.get('personality_profiles', {})
        
        section = """
        <div class="section">
            <div class="section-title">🧠 Personality Profiles</div>
        """
        
        for person, traits in profiles.items():
            section += f"""
            <div class="participant-card">
                <div class="participant-name">{person}</div>
                <div class="trait">
                    <span class="trait-icon">📝</span>
                    <span>{traits.get('communication_style', 'Communicator')}</span>
                </div>
                <div class="trait">
                    <span class="trait-icon">⚡</span>
                    <span>{traits.get('response_style', 'Responder')}</span>
                </div>
                <div class="trait">
                    <span class="trait-icon">💭</span>
                    <span>{traits.get('texting_pattern', 'Texter')}</span>
                </div>
                <div class="trait">
                    <span class="trait-icon">😊</span>
                    <span>{traits.get('expression_style', 'Expressive')}</span>
                </div>
                <div class="trait">
                    <span class="trait-icon">🚀</span>
                    <span>{traits.get('initiation_style', 'Initiator')}</span>
                </div>
            </div>
            """
        
        section += "</div>"
        return section
    
    def _generate_behavioral_indicators(self, data: Dict) -> str:
        """Generate behavioral indicators section"""
        # Get tone and content analysis
        tone_analysis = data.get('tone_analysis', {})
        content_analysis = data.get('content_analysis', {})
        
        # Build dynamic indicators list
        indicators = []
        
        # Tone indicators
        casual_pct = tone_analysis.get('casual_percentage', 0)
        if casual_pct > 20:
            indicators.append(f"Very casual/slang language ({casual_pct:.1f}%) - typical of close friendships")
        elif casual_pct > 10:
            indicators.append(f"Moderate casual language ({casual_pct:.1f}%) - comfortable relationship")
        
        formal_pct = tone_analysis.get('formal_percentage', 0)
        if formal_pct > 15:
            indicators.append(f"Formal/polite language ({formal_pct:.1f}%) - professional or new relationship")
        
        insult_pct = tone_analysis.get('insult_percentage', 0)
        roasting_pct = tone_analysis.get('roasting_percentage', 0)
        if roasting_pct > 1 or insult_pct > 2:
            indicators.append(f"Playful roasting/insults detected ({roasting_pct:.1f}%) - close friends who joke around")
        
        # Content indicators
        shared_parent_pct = content_analysis.get('shared_parent_percentage', 0)
        if shared_parent_pct > 2:
            indicators.append(f"⭐ Frequent shared parent references ({shared_parent_pct:.1f}%) - STRONG sibling indicator!")
        elif shared_parent_pct > 0.5:
            indicators.append(f"Shared parent discussions ({shared_parent_pct:.1f}%) - possible siblings")
        
        future_life_pct = content_analysis.get('future_life_percentage', 0)
        if future_life_pct > 1:
            indicators.append(f"⭐ Life planning discussions ({future_life_pct:.1f}%) - serious romantic or family relationship")
        elif future_life_pct > 0.3:
            indicators.append(f"Future life discussions ({future_life_pct:.1f}%) - long-term relationship")
        
        future_living_pct = content_analysis.get('future_living_percentage', 0)
        if future_living_pct > 0.5:
            indicators.append(f"Living together discussions ({future_living_pct:.1f}%) - roommates or romantic partners")
        
        future_business_pct = content_analysis.get('future_business_percentage', 0)
        if future_business_pct > 1:
            indicators.append(f"Business planning ({future_business_pct:.1f}%) - work partners or entrepreneurs")
        
        future_travel_pct = content_analysis.get('future_travel_percentage', 0)
        if future_travel_pct > 1:
            indicators.append(f"Travel planning together ({future_travel_pct:.1f}%) - close relationship")
        
        # Additional behavioral indicators from data
        greetings = data.get('total_greetings', 0)
        if greetings > 10:
            indicators.append(f"Regular good morning/night greetings ({greetings} times) - intimate behavior")
        
        affection = data.get('total_affection', 0)
        if affection > 20:
            indicators.append(f"Frequent affectionate language ({affection} times) - romantic or very close")
        
        night_pct = data.get('night_percentage', 0)
        if night_pct > 20:
            indicators.append(f"High late-night messaging ({night_pct:.1f}%) - close relationship")
        
        # Fallback to romantic indicators if no other data
        if not indicators:
            indicators = data.get('romantic_indicators', ['Analysis based on communication patterns'])
        
        section = f"""
        <div class="section">
            <div class="section-title">🔍 Behavioral Indicators & Key Signals</div>
            <div class="emoji-large">{"✅" if len(indicators) >= 5 else "📊"}</div>
            
            <div class="indicator-list">
                <h3 style="margin-bottom: 15px;">Detected Patterns ({len(indicators)} key indicators)</h3>
        """
        
        for i, indicator in enumerate(indicators, 1):
            section += f"""
                <div class="indicator-item">
                    <div class="indicator-number">{i}</div>
                    <div>{indicator}</div>
                </div>
            """
        
        section += """
            </div>
        </div>
        """
        
        return section
    
    def _generate_final_judgment(self, data: Dict) -> str:
        """Generate final judgment section"""
        conclusion = data.get('conclusion', 'Analysis complete.')
        
        # Get relationship scores and find top type
        relationship_scores = data.get('relationship_scores', {})
        relationship_type_map = data.get('relationship_type_map', {})
        
        if relationship_scores:
            top_type = max(relationship_scores, key=relationship_scores.get)
            top_score = relationship_scores[top_type]
            top_label = relationship_type_map.get(top_type, top_type.replace('_', ' ').title())
            emoji_map = {
                'romantic_dating': '💕',
                'romantic_established': '❤️',
                'close_friends': '👥',
                'casual_friends': '🤝',
                'family_sibling': '👨‍👩‍👧‍👦',
                'family_parent': '👨‍👩‍👧',
                'colleagues': '💼',
                'work_professional': '🏢',
                'boss_subordinate': '👔',
                'acquaintances': '👋',
                'enemy_conflict': '⚔️',
                'new_acquaintance': '✨'
            }
            top_emoji = emoji_map.get(top_type, '📊')
            indicator_text = f"{top_emoji} {top_label} Relationship (Confidence: {top_score})"
        else:
            # Fallback
            romantic_indicators = len(data.get('romantic_indicators', []))
            indicator_text = f"{romantic_indicators} Romantic Indicators Detected"
        
        return f"""
        <div class="section">
            <div class="section-title">⚖️ Final Analysis</div>
            
            <div class="judgment-box" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                <div class="judgment-title">Conclusion</div>
                <div class="judgment-content">
                    {conclusion}
                </div>
                <div style="text-align: center; margin-top: 20px;">
                    <div class="score-badge" style="background: rgba(255,255,255,0.2); font-size: 1.1em;">
                        {indicator_text}
                    </div>
                </div>
            </div>
            
            <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 10px;">
                <h3 style="margin-bottom: 15px;">📝 Key Takeaways</h3>
                <ul style="list-style: none; padding: 0;">
                    {self._generate_key_takeaways(data)}
                </ul>
            </div>
        </div>
        """
    
    def _generate_key_takeaways(self, data: Dict) -> str:
        """Generate key takeaways list"""
        takeaways = []
        
        # Get relationship context
        relationship_scores = data.get('relationship_scores', {})
        relationship_type_map = data.get('relationship_type_map', {})
        tone_analysis = data.get('tone_analysis', {})
        content_analysis = data.get('content_analysis', {})
        
        # Determine top relationship type
        top_type = None
        if relationship_scores:
            top_type = max(relationship_scores, key=relationship_scores.get)
        
        # Communication frequency
        msgs_per_day = data.get('msgs_per_day', 0)
        if msgs_per_day > 50:
            if top_type and 'romantic' in top_type:
                takeaways.append("Extremely high communication frequency indicates strong romantic interest")
            elif top_type and 'close' in top_type:
                takeaways.append("Extremely high communication frequency shows deep friendship bond")
            else:
                takeaways.append("Extremely high communication frequency indicates strong mutual engagement")
        
        # Duration
        duration = data.get('duration_days', 0)
        if duration < 90:
            takeaways.append("Recent relationship start suggests early/exploratory phase")
        elif duration > 365:
            takeaways.append("Long-term relationship spanning over a year shows sustained connection")
        
        # Tone-based insights
        casual_pct = tone_analysis.get('casual_percentage', 0)
        if casual_pct > 25:
            takeaways.append("Very casual communication style indicates comfortable, authentic relationship")
        
        formal_pct = tone_analysis.get('formal_percentage', 0)
        if formal_pct > 15:
            takeaways.append("Formal language suggests professional boundaries or new relationship")
        
        roasting_pct = tone_analysis.get('roasting_percentage', 0)
        if roasting_pct > 2:
            takeaways.append("Playful roasting and banter typical of close friends who joke around")
        
        # Content-based insights
        shared_parent_pct = content_analysis.get('shared_parent_percentage', 0)
        if shared_parent_pct > 2:
            takeaways.append("⭐ Frequent parent references strongly suggest sibling relationship!")
        
        future_life_pct = content_analysis.get('future_life_percentage', 0)
        if future_life_pct > 1:
            takeaways.append("Life planning discussions indicate serious long-term commitment")
        
        # Night communication
        night_pct = data.get('night_percentage', 0)
        if night_pct > 20:
            takeaways.append("Significant late-night communication shows prioritization and comfort")
        
        # Greetings
        greetings = data.get('total_greetings', 0)
        if greetings > 10:
            takeaways.append("Regular good morning/night rituals indicate intimate connection")
        
        if not takeaways:
            takeaways.append("Balanced and healthy communication patterns detected")
        
        html = ""
        for takeaway in takeaways:
            html += f'<li style="margin: 10px 0; padding-left: 25px; position: relative;"><span style="position: absolute; left: 0;">•</span>{takeaway}</li>'
        
        return html

    def _generate_compact_html(self, data: Dict[str, Any]) -> str:
        """Generate a compact, single-page card format HTML"""
        
        # Get key data
        relationship_scores = data.get('relationship_scores', {})
        relationship_type_map = data.get('relationship_type_map', {})
        tone_analysis = data.get('tone_analysis', {})
        
        # Get top relationship type
        top_type = max(relationship_scores, key=relationship_scores.get) if relationship_scores else 'unknown'
        top_score = relationship_scores.get(top_type, 0)
        top_label = relationship_type_map.get(top_type, data.get('relationship_type', 'Unknown'))
        
        emoji_map = {
            'romantic_dating': '💕',
            'romantic_established': '❤️',
            'close_friends': '👥',
            'casual_friends': '🤝',
            'family_sibling': '👨‍👩‍👧‍👦',
            'family_parent': '👨‍👩‍👧',
            'colleagues': '💼',
            'work_professional': '🏢',
            'boss_subordinate': '👔',
            'acquaintances': '👋',
            'enemy_conflict': '⚔️',
            'new_acquaintance': '✨'
        }
        top_emoji = emoji_map.get(top_type, '📊')
        
        participants = data.get('participants', [])
        participant_display = ', '.join(participants) if len(participants) <= 4 else f"{len(participants)} people"
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WhatsApp Relationship Card</title>
    <style>
        @media print {{
            @page {{ size: A4; margin: 0; }}
            body {{ margin: 0; padding: 20px; }}
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .card {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            max-width: 800px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #f0f0f0;
        }}
        
        .emoji-large {{
            font-size: 60px;
            margin-bottom: 10px;
        }}
        
        .relationship-type {{
            font-size: 28px;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .confidence {{
            font-size: 14px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
            margin: 25px 0;
        }}
        
        .stat-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 12px;
            color: white;
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 32px;
            font-weight: bold;
            display: block;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            font-size: 12px;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .insights {{
            margin-top: 25px;
        }}
        
        .insight-item {{
            background: #f8f9fa;
            padding: 12px 15px;
            margin: 8px 0;
            border-radius: 8px;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .insight-icon {{
            font-size: 20px;
        }}
        
        .scores-section {{
            margin-top: 25px;
            padding-top: 20px;
            border-top: 2px solid #f0f0f0;
        }}
        
        .score-bar {{
            margin: 10px 0;
        }}
        
        .score-label {{
            font-size: 13px;
            margin-bottom: 5px;
            display: flex;
            justify-content: space-between;
        }}
        
        .progress-bar {{
            height: 6px;
            background: #e0e0e0;
            border-radius: 3px;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s ease;
        }}
        
        .footer {{
            margin-top: 25px;
            padding-top: 20px;
            border-top: 2px solid #f0f0f0;
            text-align: center;
            font-size: 12px;
            color: #999;
        }}
    </style>
</head>
<body>
    <div class="card">
        <div class="header">
            <div class="emoji-large">{top_emoji}</div>
            <div class="relationship-type">{top_label}</div>
            <div class="confidence">Confidence: {data.get('confidence_level', 'MODERATE')} ({top_score})</div>
            <div style="margin-top: 10px; font-size: 14px; color: #666;">{data.get('relationship_interpretation', '')}</div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-box">
                <span class="stat-value">{data.get('total_messages', 0):,}</span>
                <span class="stat-label">Messages</span>
            </div>
            <div class="stat-box">
                <span class="stat-value">{data.get('duration_days', 0)}</span>
                <span class="stat-label">Days</span>
            </div>
            <div class="stat-box">
                <span class="stat-value">{data.get('msgs_per_day', 0):.0f}</span>
                <span class="stat-label">Msgs/Day</span>
            </div>
            <div class="stat-box">
                <span class="stat-value">{len(participants)}</span>
                <span class="stat-label">People</span>
            </div>
        </div>
        
        <div class="insights">
            <strong style="font-size: 16px; display: block; margin-bottom: 10px;">📊 Key Insights</strong>
            
            <div class="insight-item">
                <span class="insight-icon">🗣️</span>
                <span>Casual: {tone_analysis.get('casual_percentage', 0):.1f}% | Formal: {tone_analysis.get('formal_percentage', 0):.1f}%</span>
            </div>
            
            <div class="insight-item">
                <span class="insight-icon">💬</span>
                <span>{"Group chat" if len(participants) > 2 else "One-on-one"} conversation{" with " + participant_display if len(participants) <= 4 else ""}</span>
            </div>
            
            {self._get_compact_key_insight(data)}
        </div>
        
        <div class="scores-section">
            <strong style="font-size: 16px; display: block; margin-bottom: 15px;">🎯 Relationship Scores</strong>
            {self._generate_compact_scores(relationship_scores, relationship_type_map)}
        </div>
        
        <div class="footer">
            <p>WhatsApp Friendship Analyzer | Generated {datetime.now().strftime('%B %d, %Y')}</p>
            <p style="margin-top: 5px;">Participants: {participant_display}</p>
        </div>
    </div>
</body>
</html>"""

    def _get_compact_key_insight(self, data: Dict) -> str:
        """Generate a single key insight for compact card"""
        tone_analysis = data.get('tone_analysis', {})
        content_analysis = data.get('content_analysis', {})
        
        casual_pct = tone_analysis.get('casual_percentage', 0)
        future_life_pct = content_analysis.get('future_life_percentage', 0)
        shared_parent_pct = content_analysis.get('shared_parent_percentage', 0)
        night_pct = data.get('night_percentage', 0)
        
        if len(data.get('participants', [])) > 2:
            return '<div class="insight-item"><span class="insight-icon">👥</span><span>Active group dynamic with regular participation</span></div>'
        elif shared_parent_pct > 2:
            return '<div class="insight-item"><span class="insight-icon">⭐</span><span>Strong sibling indicators detected</span></div>'
        elif future_life_pct > 1:
            return '<div class="insight-item"><span class="insight-icon">🔮</span><span>Serious future planning discussions</span></div>'
        elif casual_pct > 25:
            return '<div class="insight-item"><span class="insight-icon">😎</span><span>Very casual and comfortable communication</span></div>'
        elif night_pct > 20:
            return '<div class="insight-item"><span class="insight-icon">🌙</span><span>Frequent late-night conversations</span></div>'
        else:
            return '<div class="insight-item"><span class="insight-icon">💭</span><span>Consistent and balanced communication</span></div>'
    
    def _generate_compact_scores(self, scores: Dict, type_map: Dict) -> str:
        """Generate compact score bars for top 3 relationships"""
        if not scores:
            return ""
        
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
        max_score = max(scores.values()) if scores else 100
        
        html = ""
        for rel_type, score in sorted_scores:
            label = type_map.get(rel_type, rel_type.replace('_', ' ').title())
            percentage = (score / max_score * 100) if max_score > 0 else 0
            
            html += f"""
            <div class="score-bar">
                <div class="score-label">
                    <span>{label}</span>
                    <span>{score}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {percentage}%"></div>
                </div>
            </div>
            """
        
        return html
