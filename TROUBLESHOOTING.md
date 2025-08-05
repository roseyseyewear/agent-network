# Troubleshooting Guide

## Quick Diagnostic Checklist

### Before You Start
- [ ] Python 3.10+ installed and working
- [ ] All packages installed: `pip install -r requirements.txt`
- [ ] CLAUDE.md configuration file created
- [ ] Scripts can import without errors: `python -c "import autonomous_working_agents"`

## Common Setup Issues

### Installation Problems

**Issue**: `ModuleNotFoundError: No module named 'requests'`
**Solution**:
```bash
pip install requests python-dotenv
# Or if using Python 3 specifically:
python3 -m pip install requests python-dotenv
```

**Issue**: `Python not found` or version too old
**Solution**:
1. Install Python 3.10+ from python.org
2. Verify installation: `python --version`
3. Use `python3` if `python` points to older version

**Issue**: Permission errors when installing packages
**Solution**:
```bash
# On Windows:
pip install --user requests python-dotenv

# On Mac/Linux:
python3 -m pip install --user requests python-dotenv
```

### Configuration Issues

**Issue**: Agents don't understand business context
**Symptoms**: Generic responses, irrelevant recommendations, asks basic questions repeatedly
**Solution**:
1. Check that CLAUDE.md file exists in script directory
2. Verify file contains specific business details, not template placeholders
3. Add more context about your industry, customers, and current priorities
4. Include examples of good vs. bad decisions for your business

**Issue**: `FileNotFoundError` when running scripts
**Solution**:
1. Make sure you're running scripts from the correct directory
2. Check that all files were copied properly from the package
3. Verify file permissions allow reading and writing

### Agent Performance Issues

**Issue**: Agents produce low-quality or irrelevant work
**Symptoms**: Generic advice, no specific recommendations, missing business context
**Troubleshooting Steps**:
1. **Check Business Configuration**
   - Is CLAUDE.md complete with specific details?
   - Does it include your actual business model and priorities?
   - Are industry-specific details included?

2. **Test with Specific Tasks**
   - Start with very specific, clear task descriptions
   - Example: "Research project management tools for a 5-person marketing agency" vs. "Research tools"

3. **Adjust Quality Thresholds**
   - Temporarily lower confidence threshold from 70% to 50%
   - Check what agents produce at lower thresholds
   - Gradually increase as you refine the system

**Issue**: Agents take too long or seem to hang
**Symptoms**: No output for extended periods, high CPU usage, scripts don't complete
**Solution**:
1. **Check System Resources**
   - Close other applications using CPU/memory
   - Verify sufficient disk space for output files
   - Monitor task manager during agent execution

2. **Start with Fewer Agents**
   - Test one agent type at a time
   - Reduce number of simultaneous agents
   - Gradually scale up as system proves stable

3. **Simplify Tasks**
   - Use shorter, more specific task descriptions
   - Break complex tasks into smaller components
   - Test with simple tasks before complex workflows

## Integration Problems

### ClickUp Integration Issues

**Issue**: `Unauthorized` or `Invalid API key` errors
**Solution**:
1. **Verify API Key**
   - Log into ClickUp → Settings → Apps → Generate API Key
   - Copy exact key to `.env` file: `CLICKUP_API_KEY=pk_your_key_here`
   - No quotes around the key value

2. **Check Permissions**
   - API key must have read access to your tasks
   - Test with simple API call: `python clickup_analysis_tools/clickup_integration.py`

3. **Update List IDs**
   - Find your ClickUp list IDs in the URL when viewing lists
   - Update `hannah_list_id` in scripts to match your lists

**Issue**: Tasks not found or empty results
**Solution**:
1. Verify list IDs are correct for your ClickUp workspace
2. Check that lists contain tasks (system can't analyze empty lists)
3. Ensure API key has access to the specific lists you're trying to read

### File Access Issues

**Issue**: `PermissionError` when writing files
**Solution**:
1. **Check Directory Permissions**
   ```bash
   # Create a test file to verify write access
   echo "test" > test_write.txt
   rm test_write.txt
   ```

2. **Run from User Directory**
   - Don't run scripts from system directories
   - Use your user folder or desktop for testing

3. **Verify File Locks**
   - Close any files that might be open in other applications
   - Check that no other processes are using the script directory

## Agent-Specific Issues

### Research Agent Problems

**Issue**: Research lacks depth or sources
**Solution**:
- Add specific research requirements to agent instructions
- Include examples of good research reports in configuration
- Specify minimum number of sources required

**Issue**: Research not relevant to business
**Solution**:
- Include more industry context in CLAUDE.md
- Add competitor information and market positioning
- Specify research focus areas and what to avoid

### Business Analysis Agent Problems

**Issue**: Analysis too generic or theoretical
**Solution**:
- Include specific business metrics and KPIs in configuration
- Add context about past business decisions and outcomes
- Specify analysis frameworks preferred for your industry

**Issue**: Recommendations not actionable
**Solution**:
- Include examples of previous successful initiatives
- Specify resource constraints and budget considerations
- Add timeline preferences and implementation capacity

### Vendor Selection Agent Problems

**Issue**: Vendor recommendations not suitable
**Solution**:
- Include budget ranges and service requirements
- Add geographic or industry-specific constraints
- Specify evaluation criteria important to your business

## Performance Optimization

### Speed Improvements

**Issue**: System runs slowly
**Solutions**:
1. **Reduce Simultaneous Agents**
   ```python
   # In autonomous_working_agents.py
   # Start with 2-3 agents instead of 5
   ```

2. **Optimize Task Descriptions**
   - Use specific, focused task descriptions
   - Avoid overly broad or complex requests
   - Break large tasks into smaller components

3. **System Resources**
   - Close unnecessary applications
   - Ensure adequate RAM (8GB+ recommended)
   - Use SSD storage if available

### Quality Improvements

**Issue**: Inconsistent work quality
**Solutions**:
1. **Refine Business Configuration**
   - Add more specific examples of good work
   - Include quality standards and expectations
   - Specify industry best practices and standards

2. **Adjust Quality Thresholds**
   ```python
   # In _assess_readiness_for_founder_review method
   if assessment['confidence_score'] >= 0.8:  # Raise from 0.7 for higher quality
   ```

3. **Add Quality Indicators**
   - Specify required elements for each task type
   - Include examples of comprehensive analysis
   - Define minimum standards for recommendations

## Advanced Troubleshooting

### Debug Mode

Enable detailed logging for troubleshooting:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Add this to the top of any script for detailed output.

### Custom Agent Development

If agents don't meet your needs, create custom versions:
```python
class CustomBusinessAgent(AutonomousWorkingAgent):
    def _execute_task_work(self, task):
        # Your custom business logic here
        return {
            'task_id': task['id'],
            'custom_analysis': self._your_method(task),
            'recommendations': self._generate_recs(task)
        }
```

### Performance Monitoring

Track system performance:
```python
import time

start_time = time.time()
# Agent work here
end_time = time.time()
print(f"Execution time: {end_time - start_time:.2f} seconds")
```

## Getting Additional Help

### Self-Diagnosis Steps
1. **Test Individual Components**
   - Run each script separately
   - Test agents individually before combining
   - Verify each integration point works

2. **Check Error Messages**
   - Read full error messages, not just the last line
   - Search for specific error text online
   - Check Python and package versions

3. **Verify Environment**
   - Test in clean directory with minimal setup
   - Check for conflicting Python installations
   - Verify all dependencies are correct versions

### When to Ask Your Claude for Help
- Configuration and customization questions
- Business-specific adaptations
- Performance optimization for your use case
- Integration with your specific tools and workflows

### Documentation to Review
- README.md: Complete overview and examples
- SETUP_GUIDE.md: Step-by-step implementation
- CONFIGURATION_TEMPLATE.md: Business setup examples
- Source code: All scripts are readable and well-commented

### Common Patterns
- **Start Simple**: Test basic functionality before complex workflows
- **Isolate Issues**: Test components individually to identify problems
- **Check Configuration**: Most issues stem from incomplete business context
- **Monitor Performance**: Track what works and optimize based on results

---

## Error Code Reference

### Import Errors
- `ModuleNotFoundError`: Missing Python packages - run `pip install -r requirements.txt`
- `ImportError`: Version conflicts - check Python version and package versions

### Runtime Errors  
- `FileNotFoundError`: Missing files or incorrect paths
- `PermissionError`: File access issues - check directory permissions
- `ConnectionError`: Network issues - check internet connection and API endpoints

### API Errors
- `401 Unauthorized`: Invalid API keys - check credentials in `.env` file
- `403 Forbidden`: Insufficient permissions - verify API key access levels
- `404 Not Found`: Invalid IDs - check ClickUp list IDs and URLs

### Business Logic Errors
- Low confidence scores: Insufficient business context - expand CLAUDE.md
- Generic responses: Vague task descriptions - be more specific
- Poor quality: Missing examples - add success/failure examples to configuration

---

**Remember**: Most issues are configuration-related. Start with business context and work toward technical details. Your Claude can help diagnose and resolve most problems through interactive troubleshooting.