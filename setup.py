#!/usr/bin/env python3
"""
Setup script for Ultimate SEO Analysis Tool
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements from requirements.txt
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ultimate-seo-analyzer",
    version="1.0.0",
    author="Ultimate SEO Analyzer Team",
    author_email="contact@ultimate-seo-analyzer.com",
    description="The most comprehensive free and open-source SEO analysis tool",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ultimate-seo-analyzer",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ultimate-seo-analyzer/issues",
        "Source": "https://github.com/yourusername/ultimate-seo-analyzer",
        "Documentation": "https://github.com/yourusername/ultimate-seo-analyzer/blob/main/USAGE.md",
        "Changelog": "https://github.com/yourusername/ultimate-seo-analyzer/blob/main/CHANGELOG.md",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "bandit>=1.7.0",
            "safety>=2.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.18.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ultimate-seo-analyzer=ultimate_seo_analyzer:main",
            "seo-analyzer=seo_analyzer:main",
            "bulk-seo-analyzer=bulk_analyzer:main",
            "competitor-analyzer=competitor_analyzer:main",
            "sitemap-generator=sitemap_generator:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    keywords=[
        "seo",
        "analysis",
        "website",
        "optimization",
        "search-engine",
        "ai",
        "openai",
        "competitor-analysis",
        "sitemap",
        "web-scraping",
        "performance",
        "accessibility",
        "security",
        "content-analysis",
        "technical-seo",
        "aeo",
        "geo",
        "voice-search",
        "featured-snippets",
    ],
    zip_safe=False,
)